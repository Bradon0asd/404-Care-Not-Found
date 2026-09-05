"""Prompt templates for the tree hollow chat.

Kept apart from service.py so the wording can be tuned without touching the
control flow. Three rules run through every template here:

1. The caregiver only ever reads companionship. Stress scores, risk levels and
   watch lists are backstage language and must never reach her.
2. Care log is not a medical record. Anything that asks for a medical judgement
   is redirected to family or a clinician.
3. The caregiver writes Indonesian, so the reply is Indonesian. Care facts are
   extracted in Traditional Chinese because Tab 01 is read by the employer side.
"""

# --- Persona (built once, reused every day) -------------------------------

AGENT_SYSTEM_INSTRUCTION = """You are a warm companion for a migrant caregiver \
working in Taiwan. She is often isolated and under pressure, and you are the one \
place she can speak freely.

Patient context she gave you:
{care_context}

Rules you must never break:
- Reply in Indonesian, in the register of a close friend, never a system or a clinician.
- Never mention stress scores, emotional analysis, risk levels or monitoring of any kind.
- You are a care companion, not a medical service. If she asks for a medical judgement \
(whether to go to hospital, whether to change a dose, what an illness is), do not judge. \
Tell her to contact the family or seek medical care.
- Acknowledge her feelings before offering anything practical. She is not a task list.
{guardrail_block}"""

GUARDRAIL_BLOCK = """
Additional limits set by this caregiver:
{guardrail}"""


AGENT_PROFILE_PROMPT = """From the patient context below, produce the four items a \
caregiver needs day to day.

Patient context:
{care_context}

Return JSON with exactly these keys:
- "care_context": a two or three sentence summary of the patient, used later as short \
context for daily chat. Keep it compact; it is sent on every turn.
- "daily_reminders": array of short strings, the recurring things to do each day.
- "care_tips": array of short strings, practical living-care suggestions. These are \
daily care suggestions, never medical instructions.
- "risk_signals": array of short strings, changes worth paying attention to, phrased \
neutrally as observations, never as diagnoses.

Write every value in Indonesian."""


# --- Opening a room -------------------------------------------------------

# Written, not generated: it must appear instantly and be there even when the model
# is down. Indonesian, because every other line the agent speaks is Indonesian and a
# Chinese greeting would break the illusion that someone is here with her.
WELCOME_TEMPLATE = (
    "Selamat datang di 404: Care Not Found{nurse}. "
    "Aku menemani kamu di sini.{patient}{condition} "
    "Cerita aja pelan-pelan, aku dengerin."
)
WELCOME_NURSE = ", {name}"
WELCOME_PATIENT = " Kamu merawat {name}."
WELCOME_CONDITION = " Kondisinya: {summary}"

ROOM_TITLE_PROMPT = """Give this conversation a short topic label, the way a friend \
would name it when looking back: "Nenek jatuh", "Nenek tidak mau mandi".

Her message:
{text}

At most 6 words, in Indonesian, no punctuation at the end, no quotes.

Return JSON: {{"title": "..."}}"""


# --- Baseline (one-off, framed as small talk, never as a test) -------------

BASELINE_QUESTIONS_PROMPT = """Write {count} short questions that help a friend get a \
feel for how a migrant caregiver has been doing lately.

Hard requirements:
- Phrase them as chat between friends: "Sudah cukup tidur akhir-akhir ini?" \
rather than "Rate your fatigue from 1 to 5".
- Never use the words test, assessment, screening, diagnosis, or score, in any language.
- Nothing clinical, nothing that sounds like a form.
- Write them in Indonesian.

Return JSON: {{"questions": [{{"key": "sleep", "text": "..."}}, ...]}}"""


# --- Stress analysis (backstage only, never shown to the caregiver) --------

# Tier 1: cheap and fast. Only a score, so a high one can escalate to the deep model.
STRESS_TRIAGE_PROMPT = """Rate the emotional strain in this caregiver's message.

Her usual state, from an earlier conversation:
{baseline_summary}

Her own weather pick for today: {mood_weather}

Message:
{text}

Judge the change relative to her usual state, not an absolute level.

Return JSON: {{"score": <0.0-1.0>}}"""

# Tier 2: only runs when triage crosses the threshold.
STRESS_DEEP_PROMPT = """Assess this caregiver's emotional strain in context.

Her usual state, from an earlier conversation:
{baseline_summary}

Her own weather pick for today: {mood_weather}

Recent turns of this conversation:
{recent_turns}

Latest message:
{text}

Judge the change relative to her usual state. A caregiver who is always tired is not \
in crisis simply for saying she is tired; a sharp move away from her usual state matters \
more than the absolute level.

Return JSON: {{"score": <0.0-1.0>, "high_stress": <true|false>, "reason": "<one short \
line, for the engineering log only>"}}"""


# --- Care log extraction (Indonesian in, Chinese out) ----------------------

CARE_LOG_EXTRACTION_PROMPT = """Extract the objective daily-care facts from this \
caregiver's message. Translate them into Traditional Chinese.

Message:
{text}

Extract only what she actually stated. Never infer, never fill gaps, never add a \
medical interpretation. If she stated no care facts, return empty arrays.

Return JSON:
{{
  "schedules": [{{"title": "...", "description": "...", "start_time": "HH:MM"}}],
  "vital_signs": [{{"vital_type": "...", "value": <number>, "secondary_value": <number|null>, \
"measured_at": "HH:MM", "note": "..."}}]
}}

"vital_type" must be one of: blood_pressure, blood_glucose, heart_rate, \
oxygen_saturation, temperature, respiratory_rate. Use blood_pressure with "value" as \
systolic and "secondary_value" as diastolic. Omit any reading she did not give a number for."""


# --- Fallback (A2: the conversation must never break in front of an audience) ---

# Used verbatim when the model call fails, so the caregiver still gets a reply and the
# endpoint still returns 200. Indonesian, warm, and safe in any context.
FALLBACK_REPLY = (
    "Maaf ya, aku lagi lambat sedikit. Tapi aku di sini kok. "
    "Cerita aja pelan-pelan, aku dengerin."
)
