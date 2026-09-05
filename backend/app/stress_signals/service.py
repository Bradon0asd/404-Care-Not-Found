"""Detect strain, record the signal, and tell the employer a count.

Nothing in this module returns anything to the caregiver. Everything it produces is
backstage language, and the only thing that ever leaves it is a number and a time.
"""

import json
import logging
from datetime import datetime, time, timedelta

from flask import current_app

# The Gemini wrapper lives in app/chat/client.py, mirroring app/line/client.py. It is a
# plain HTTP client with no chat semantics, so borrowing it here does not make this
# module depend on Tab 03's logic.
from app.chat.client import GeminiClient
from app.chat.prompts import STRESS_DEEP_PROMPT, STRESS_TRIAGE_PROMPT
from app.extensions import db
from app.line.notifications import notify_stress_signal
from app.models import CareAgent, StressEvent, StressSource
from app.models.diary import utc_now
from app.shared.errors import AppError


logger = logging.getLogger(__name__)

# Only a message that clears this escalates to the expensive model. Everything below it
# costs one cheap call and stops there, which is the whole point of tiered inference.
TRIAGE_THRESHOLD = 0.5
# What the deep pass has to reach before the employer is told anything at all.
HIGH_STRESS_THRESHOLD = 0.7

NO_BASELINE = "No baseline recorded yet; judge the message on its own terms."


def analyze_and_record(
    *,
    nurse,
    text,
    source,
    baseline_summary=None,
    mood_weather=None,
    recent_turns=None,
    occurred_at=None,
):
    """Judge one piece of writing and, if it reads as high strain, raise a signal.

    Returns True when a signal was raised. Callers use the return value for logging
    only; nothing here is ever surfaced to the caregiver.
    """
    if not is_high_stress(
        text=text,
        baseline_summary=baseline_summary or baseline_summary_for(nurse),
        mood_weather=mood_weather,
        recent_turns=recent_turns,
    ):
        return False

    event = record_event(nurse=nurse, source=source, occurred_at=occurred_at)
    notify_daily_total(nurse=nurse, occurred_at=event.occurred_at)
    return True


def is_high_stress(*, text, baseline_summary=None, mood_weather=None, recent_turns=None):
    """Cheap pass first; only a suspicious score pays for the deep pass."""
    baseline = baseline_summary or NO_BASELINE
    weather = mood_weather or "not given"

    triage = _ask_for_json(
        prompt=STRESS_TRIAGE_PROMPT.format(
            baseline_summary=baseline,
            mood_weather=weather,
            text=text,
        ),
        model=current_app.config.get("GEMINI_MODEL_FAST"),
        # A rating task wants the same answer every time, not a creative one.
        temperature=0,
    )
    if triage is None:
        return False

    if _as_score(triage.get("score")) < TRIAGE_THRESHOLD:
        return False

    deep = _ask_for_json(
        prompt=STRESS_DEEP_PROMPT.format(
            baseline_summary=baseline,
            mood_weather=weather,
            recent_turns=recent_turns or "(none)",
            text=text,
        ),
        model=current_app.config.get("GEMINI_MODEL_DEEP"),
        temperature=0,
    )
    if deep is None:
        return False

    # The reason is for the engineering log only and is never stored or pushed.
    logger.info("stress deep pass: score=%s reason=%s", deep.get("score"), deep.get("reason"))
    return bool(deep.get("high_stress")) or _as_score(deep.get("score")) >= HIGH_STRESS_THRESHOLD


def baseline_summary_for(nurse):
    """Her usual state, so the analysis judges a change rather than an absolute level.

    Lives here rather than in `chat` because both callers need it, and a diary must
    never have to import Tab 03 to be read against her baseline.
    """
    agent = CareAgent.query.filter_by(user_id=nurse.id).first()
    if agent is None or not agent.baseline_answers:
        return None
    return "; ".join(
        f"{answer.get('key')}: {answer.get('answer')}"
        for answer in agent.baseline_answers
        if isinstance(answer, dict)
    )


def record_event(*, nurse, source, occurred_at=None):
    if source not in (StressSource.CHAT.value, StressSource.DIARY.value):
        raise ValueError(f"Unknown stress source: {source}")

    event = StressEvent(
        nurse_id=nurse.id,
        source=source,
        occurred_at=occurred_at or utc_now(),
    )
    db.session.add(event)
    db.session.commit()
    return event


def notify_daily_total(*, nurse, occurred_at=None):
    """Push the running total for the day, once per new event rather than per message.

    The employer gets a count and a time. Events already covered by an earlier push
    are marked, so a quiet day never produces a second identical notice.
    """
    moment = occurred_at or utc_now()
    pending = _unnotified_events(nurse=nurse, day=moment)
    if not pending:
        return None

    total = _daily_count(nurse=nurse, day=moment)
    try:
        notify_stress_signal(nurse=nurse, abnormal_count=total, occurred_at=moment)
    except AppError as error:
        # An unpaired nurse or a missing LINE token must not break her conversation.
        # The events stay unnotified so the next push picks them up.
        logger.warning("stress notice not delivered: nurse_id=%s %s", nurse.id, error)
        return None

    for event in pending:
        event.notified_at = utc_now()
    db.session.commit()
    return total


def _unnotified_events(*, nurse, day):
    start, end = _day_bounds(day)
    return (
        StressEvent.query.filter(
            StressEvent.nurse_id == nurse.id,
            StressEvent.notified_at.is_(None),
            StressEvent.occurred_at >= start,
            StressEvent.occurred_at < end,
        )
        .order_by(StressEvent.occurred_at)
        .all()
    )


def _daily_count(*, nurse, day):
    start, end = _day_bounds(day)
    return StressEvent.query.filter(
        StressEvent.nurse_id == nurse.id,
        StressEvent.occurred_at >= start,
        StressEvent.occurred_at < end,
    ).count()


def _day_bounds(moment):
    start = datetime.combine(moment.date(), time.min)
    return start, start + timedelta(days=1)


def _ask_for_json(*, prompt, model, temperature):
    """Return the parsed JSON, or None if the model or the parse failed.

    Analysis is best-effort by design: when it fails the caregiver still gets her
    reply, and the only cost is a signal we did not raise.
    """
    try:
        raw = GeminiClient(model=model).generate_content(
            prompt,
            temperature=temperature,
            json_mode=True,
        )
        return json.loads(raw)
    except AppError as error:
        logger.warning("stress analysis unavailable: %s", error)
    except (ValueError, TypeError) as error:
        logger.warning("stress analysis returned unparsable JSON: %s", error)
    return None


def _as_score(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0
