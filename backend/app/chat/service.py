"""The tree hollow: setup once, then talk every day.

`process_user_message()` does three things behind one reply, and the caregiver is
meant to notice only the first: companionship for her, a stress reading for the
employer notice, and care facts for Tab 01. The second and third never change what
she reads, and never delay it — if either fails, she still gets her reply.
"""

import json
import logging
from datetime import datetime, time

from flask import current_app

from app.chat.client import GeminiClient
from app.chat.prompts import (
    AGENT_PROFILE_PROMPT,
    AGENT_SYSTEM_INSTRUCTION,
    BASELINE_QUESTIONS_PROMPT,
    CARE_LOG_EXTRACTION_PROMPT,
    FALLBACK_REPLY,
    GUARDRAIL_BLOCK,
)
from app.care_schedules.service import create_schedule
from app.extensions import db
from app.models import (
    VITAL_SIGN_UNITS,
    CareAgent,
    ChatMessage,
    ChatRoom,
    MessageSender,
    ScheduleType,
    StressSource,
)
from app.models.diary import utc_now
from app.shared.errors import (
    AppError,
    BaselineRequiredError,
    CareAgentLimitReachedError,
    CareAgentNotFoundError,
    ChatRoomNotFoundError,
    ChatRoomQuotaReachedError,
    PermissionDeniedError,
)
from app.shared.permissions import get_accessible_care_recipient
from app.stress_signals import service as stress_signals
from app.vital_signs.service import create_vital_sign


logger = logging.getLogger(__name__)

# Free tier. Enforced here rather than with a database constraint so unlocking a paid
# plan later does not need a migration against the shared database.
MAX_AGENTS_PER_USER = 1
MAX_ROOMS_PER_DAY = 1

# B3: the daily prompt carries the stored patient summary plus this many recent turns,
# never the full history. This cap is the cost story; raising it undoes it.
CONTEXT_MESSAGE_LIMIT = 6

BASELINE_QUESTION_COUNT = 5


# --- Setup mode (one-off) -------------------------------------------------

def get_agent(*, current_user):
    agent = CareAgent.query.filter_by(user_id=current_user.id).first()
    if agent is None:
        raise CareAgentNotFoundError("No care agent has been set up yet")
    return agent


def find_agent(*, current_user):
    """Same lookup without the error, for callers deciding which mode to show."""
    return CareAgent.query.filter_by(user_id=current_user.id).first()


def setup_agent(*, current_user, care_recipient_id, system_prompt, temperature=0.7, guardrail=None):
    """Build the agent once. The generated profile is stored and reused every day."""
    recipient = get_accessible_care_recipient(
        current_user=current_user,
        recipient_id=care_recipient_id,
    )
    agent = find_agent(current_user=current_user)
    if agent is not None and agent.care_recipient_id != recipient.id:
        raise CareAgentLimitReachedError(
            f"The current plan allows {MAX_AGENTS_PER_USER} care agent"
        )

    if agent is None:
        agent = CareAgent(user_id=current_user.id, care_recipient_id=recipient.id)
        db.session.add(agent)

    agent.system_prompt = system_prompt
    agent.temperature = temperature
    agent.guardrail = guardrail
    agent.generated_profile = _generate_profile(system_prompt)
    db.session.commit()
    return agent


def baseline_questions(*, current_user):
    """Small talk, never a questionnaire. The wording rule lives in prompts.py."""
    get_agent(current_user=current_user)
    generated = _ask_for_json(
        prompt=BASELINE_QUESTIONS_PROMPT.format(count=BASELINE_QUESTION_COUNT),
        temperature=0.4,
    )
    questions = (generated or {}).get("questions")
    return questions if isinstance(questions, list) and questions else _fallback_questions()


def save_baseline(*, current_user, answers):
    agent = get_agent(current_user=current_user)
    agent.baseline_answers = answers
    agent.baseline_completed_at = utc_now()
    db.session.commit()
    return agent


# --- Chat mode (daily) ----------------------------------------------------

def create_room(*, current_user, title=None, mood_weather=None):
    agent = get_agent(current_user=current_user)
    if agent.baseline_completed_at is None:
        raise BaselineRequiredError("Finish the one-off setup before starting a chat")

    if _rooms_started_today(current_user) >= MAX_ROOMS_PER_DAY:
        raise ChatRoomQuotaReachedError(
            f"The current plan allows {MAX_ROOMS_PER_DAY} chat room per day"
        )

    room = ChatRoom(
        user_id=current_user.id,
        care_agent_id=agent.id,
        title=title,
        mood_weather=mood_weather,
    )
    db.session.add(room)
    db.session.commit()
    return room


def list_rooms(*, current_user):
    return (
        ChatRoom.query.filter_by(user_id=current_user.id)
        .order_by(ChatRoom.created_at.desc(), ChatRoom.id.desc())
        .all()
    )


def get_room(*, current_user, room_id):
    room = db.session.get(ChatRoom, room_id)
    if room is None:
        raise ChatRoomNotFoundError("Chat room not found")
    if room.user_id != current_user.id:
        raise PermissionDeniedError("Chat room belongs to another user")
    return room


def process_user_message(*, current_user, room_id, text):
    """One turn. Returns only what the caregiver may see."""
    room = get_room(current_user=current_user, room_id=room_id)
    agent = room.care_agent

    user_message = ChatMessage(
        room_id=room.id,
        sender=MessageSender.USER.value,
        text=text,
    )
    db.session.add(user_message)
    db.session.commit()

    reply = _companion_reply(agent=agent, room=room, text=text)
    ai_message = ChatMessage(
        room_id=room.id,
        sender=MessageSender.AI.value,
        text=reply,
    )
    db.session.add(ai_message)
    db.session.commit()

    # Backstage. Neither step may change or delay what she just read, so both are
    # best-effort and their failures never reach the caller.
    _run_quietly(
        "stress analysis",
        stress_signals.analyze_and_record,
        nurse=current_user,
        text=text,
        source=StressSource.CHAT.value,
        baseline_summary=_baseline_summary(agent),
        mood_weather=room.mood_weather,
        recent_turns=_recent_turns(room),
    )
    _run_quietly("care log extraction", _extract_care_log, agent=agent, nurse=current_user, text=text)

    return user_message, ai_message


def room_messages(*, current_user, room_id):
    room = get_room(current_user=current_user, room_id=room_id)
    return room.messages


# --- Generation helpers ---------------------------------------------------

def _companion_reply(*, agent, room, text):
    """Her reply. If the model is unavailable she still gets a warm line (A2)."""
    try:
        return GeminiClient().generate_content(
            _turn_prompt(room=room, text=text),
            system_instruction=_system_instruction(agent),
            temperature=agent.temperature,
        )
    except AppError as error:
        logger.warning("companion reply fell back: %s", error)
        return FALLBACK_REPLY


def _system_instruction(agent):
    guardrail = (agent.guardrail or "").strip()
    return AGENT_SYSTEM_INSTRUCTION.format(
        care_context=_care_context(agent),
        # B4: the caregiver's own limits ride along with the persona, every call.
        guardrail_block=GUARDRAIL_BLOCK.format(guardrail=guardrail) if guardrail else "",
    )


def _turn_prompt(*, room, text):
    recent = _recent_turns(room)
    if not recent:
        return text
    return f"Recent turns:\n{recent}\n\nHer latest message:\n{text}"


def _recent_turns(room):
    """The tail of this room only. Never the whole history (B3)."""
    recent = room.messages[-CONTEXT_MESSAGE_LIMIT:]
    return "\n".join(f"{message.sender}: {message.text}" for message in recent)


def _care_context(agent):
    profile = agent.generated_profile or {}
    # The generated summary is short by design; the raw prompt is the fallback.
    return profile.get("care_context") or agent.system_prompt


def _baseline_summary(agent):
    answers = agent.baseline_answers
    if not answers:
        return None
    return "; ".join(
        f"{answer.get('key')}: {answer.get('answer')}"
        for answer in answers
        if isinstance(answer, dict)
    )


def _generate_profile(system_prompt):
    profile = _ask_for_json(
        prompt=AGENT_PROFILE_PROMPT.format(care_context=system_prompt),
        temperature=0.4,
    )
    if profile is None:
        # Setup must not fail because the model was briefly unavailable; daily chat
        # falls back to the raw prompt as context until the agent is set up again.
        logger.warning("care agent profile could not be generated; storing none")
    return profile


# --- Care log extraction (writes into Tab 01) -----------------------------

def _extract_care_log(*, agent, nurse, text):
    extracted = _ask_for_json(
        prompt=CARE_LOG_EXTRACTION_PROMPT.format(text=text),
        temperature=0,
    )
    if not extracted:
        return

    today = utc_now()
    for entry in extracted.get("schedules") or []:
        _write_schedule(agent=agent, nurse=nurse, entry=entry, today=today)
    for entry in extracted.get("vital_signs") or []:
        _write_vital_sign(agent=agent, nurse=nurse, entry=entry, today=today)


def _write_schedule(*, agent, nurse, entry, today):
    title = (entry.get("title") or "").strip()
    if not title:
        return

    weekday = today.weekday()
    create_schedule(
        current_user=nurse,
        recipient_id=agent.care_recipient_id,
        schedule_type=(
            ScheduleType.WEEKEND.value if weekday >= 5 else ScheduleType.WEEKDAY.value
        ),
        weekday=weekday,
        start_time=_parse_clock(entry.get("start_time")) or today.time(),
        title=title[:100],
        description=entry.get("description"),
    )


def _write_vital_sign(*, agent, nurse, entry, today):
    vital_type = entry.get("vital_type")
    if vital_type not in VITAL_SIGN_UNITS or entry.get("value") is None:
        return

    clock = _parse_clock(entry.get("measured_at"))
    create_vital_sign(
        current_user=nurse,
        recipient_id=agent.care_recipient_id,
        vital_type=vital_type,
        value=float(entry["value"]),
        secondary_value=(
            float(entry["secondary_value"]) if entry.get("secondary_value") is not None else None
        ),
        measured_at=datetime.combine(today.date(), clock) if clock else today,
        note=entry.get("note"),
    )


def _parse_clock(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%H:%M").time()
    except (ValueError, TypeError):
        return None


# --- Shared plumbing ------------------------------------------------------

def _rooms_started_today(current_user):
    start = datetime.combine(utc_now().date(), time.min)
    return ChatRoom.query.filter(
        ChatRoom.user_id == current_user.id,
        ChatRoom.created_at >= start,
    ).count()


def _ask_for_json(*, prompt, temperature):
    try:
        raw = GeminiClient().generate_content(prompt, temperature=temperature, json_mode=True)
        return json.loads(raw)
    except AppError as error:
        logger.warning("model call failed: %s", error)
    except (ValueError, TypeError) as error:
        logger.warning("model returned unparsable JSON: %s", error)
    return None


def _run_quietly(label, func, **kwargs):
    """Run a backstage step so that its failure never reaches the caregiver."""
    try:
        func(**kwargs)
    except Exception:
        db.session.rollback()
        logger.exception("%s failed and was skipped", label)


def _fallback_questions():
    """Used when the model is down. Same rule: chat, never a test."""
    return [
        {"key": "sleep", "text": "Akhir-akhir ini sudah cukup tidur?"},
        {"key": "meals", "text": "Hari ini sempat makan dengan tenang?"},
        {"key": "rest", "text": "Ada waktu buat istirahat sebentar?"},
        {"key": "contact", "text": "Masih sering ngobrol sama keluarga di rumah?"},
        {"key": "mood", "text": "Belakangan ini perasaanmu gimana?"},
    ]
