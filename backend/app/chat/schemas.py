from marshmallow import Schema, fields, validate


# The one-tap weather pick that opens a chat room. It doubles as the caregiver's own
# reading of her day, which the stress analysis compares against her baseline.
MOOD_WEATHERS = ["sunny", "cloudy", "rainy", "storm"]

SENDERS = ["user", "ai"]


class CareAgentCreateSchema(Schema):
    care_recipient_id = fields.Int(required=True)
    system_prompt = fields.Str(required=True, validate=validate.Length(min=1))
    # Gemini accepts 0-2. The UI slider starts at 0, where the model is least random.
    temperature = fields.Float(load_default=0.7, validate=validate.Range(min=0, max=2))
    guardrail = fields.Str(load_default=None, allow_none=True)


class CareAgentSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    care_recipient_id = fields.Int(required=True)
    system_prompt = fields.Str(required=True)
    temperature = fields.Float(required=True)
    guardrail = fields.Str(allow_none=True)
    # The four items generated once in Step 2 and reused every day: care_context,
    # daily_reminders, care_tips, risk_signals.
    generated_profile = fields.Dict(allow_none=True)
    # Present means the caregiver has finished setup, so Tab 03 switches to chat mode.
    baseline_completed_at = fields.DateTime(allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)


class BaselineAnswerSchema(Schema):
    key = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    answer = fields.Str(required=True, validate=validate.Length(min=1))


class BaselineSubmitSchema(Schema):
    answers = fields.List(fields.Nested(BaselineAnswerSchema), required=True)


class ChatRoomCreateSchema(Schema):
    title = fields.Str(load_default=None, allow_none=True, validate=validate.Length(max=100))
    mood_weather = fields.Str(
        load_default=None,
        allow_none=True,
        validate=validate.OneOf(MOOD_WEATHERS),
    )


class ChatRoomSchema(Schema):
    id = fields.Int(required=True)
    user_id = fields.Int(required=True)
    care_agent_id = fields.Int(required=True)
    title = fields.Str(allow_none=True)
    mood_weather = fields.Str(allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)


class ChatMessageCreateSchema(Schema):
    text = fields.Str(required=True, validate=validate.Length(min=1))


class ChatMessageSchema(Schema):
    """What the caregiver reads back.

    Deliberately has no stress field of any kind. Stress scores and high-stress flags
    live in StressEvent, are backstage language, and must never reach the caregiver.
    """

    id = fields.Int(required=True)
    room_id = fields.Int(required=True)
    sender = fields.Str(required=True, validate=validate.OneOf(SENDERS))
    text = fields.Str(required=True)
    created_at = fields.DateTime(required=True)


class ChatTurnSchema(Schema):
    """One exchange: what she sent, and the companionship that came back."""

    user_message = fields.Nested(ChatMessageSchema, required=True)
    ai_message = fields.Nested(ChatMessageSchema, required=True)
