from enum import StrEnum

from app.extensions import db
from app.models.diary import utc_now


class MoodWeather(StrEnum):
    SUNNY = "sunny"
    CLOUDY = "cloudy"
    RAINY = "rainy"
    STORM = "storm"


class MessageSender(StrEnum):
    USER = "user"
    AI = "ai"


MOOD_WEATHERS = tuple(weather.value for weather in MoodWeather)
MESSAGE_SENDERS = tuple(sender.value for sender in MessageSender)


class CareAgent(db.Model):
    """The caregiver's one-off setup, generated once and reused every day.

    Everything expensive lives here: the persona built from her patient context and
    the baseline that later stress analysis compares against. Daily chat reads these
    columns instead of regenerating them, which is the whole token-cost argument.
    """

    __tablename__ = "care_agents"
    __table_args__ = (
        db.CheckConstraint(
            "temperature >= 0 AND temperature <= 2",
            name="ck_care_agents_temperature",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    # Needed to write extracted care facts into CareSchedule / VitalSignLog and to
    # greet the caregiver with the patient's details. The handover doc omitted it.
    care_recipient_id = db.Column(
        db.Integer,
        db.ForeignKey("care_recipients.id"),
        nullable=False,
        index=True,
    )
    system_prompt = db.Column(db.Text, nullable=False)
    temperature = db.Column(db.Float, nullable=False, default=0.7, server_default="0.7")
    guardrail = db.Column(db.Text, nullable=True)
    # The four items from Step 2: care_context, daily_reminders, care_tips, risk_signals.
    generated_profile = db.Column(db.JSON, nullable=True)
    baseline_answers = db.Column(db.JSON, nullable=True)
    # Set means setup is done, so Tab 03 stops showing the one-off flow for good.
    baseline_completed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
        server_default=db.func.current_timestamp(),
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=db.func.current_timestamp(),
    )

    # One-directional on purpose: User and CareRecipient are edited by others, and a
    # back_populates pair would mean touching their file for every model added here.
    user = db.relationship("User", foreign_keys=[user_id], lazy="select")
    care_recipient = db.relationship(
        "CareRecipient",
        foreign_keys=[care_recipient_id],
        lazy="select",
    )
    rooms = db.relationship(
        "ChatRoom",
        back_populates="care_agent",
        lazy="select",
        cascade="all, delete-orphan",
    )


class ChatRoom(db.Model):
    """One conversation topic, e.g. "grandma fell". The free tier allows one per day."""

    __tablename__ = "chat_rooms"
    __table_args__ = (
        db.CheckConstraint(
            "mood_weather IS NULL OR mood_weather IN ('sunny', 'cloudy', 'rainy', 'storm')",
            name="ck_chat_rooms_mood_weather",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    care_agent_id = db.Column(
        db.Integer,
        db.ForeignKey("care_agents.id"),
        nullable=False,
        index=True,
    )
    title = db.Column(db.String(100), nullable=True)
    # Her one-tap self-report for the day. Read by the stress analysis, never scored
    # back at her.
    mood_weather = db.Column(db.String(20), nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
        server_default=db.func.current_timestamp(),
        index=True,
    )
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
        server_default=db.func.current_timestamp(),
    )

    user = db.relationship("User", foreign_keys=[user_id], lazy="select")
    care_agent = db.relationship("CareAgent", back_populates="rooms", lazy="select")
    messages = db.relationship(
        "ChatMessage",
        back_populates="room",
        lazy="select",
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at",
    )


class ChatMessage(db.Model):
    """A single turn, in the caregiver's own Indonesian.

    Deliberately carries no stress column. Stress lives in StressEvent so that a
    signal can never be joined back to what she wrote.
    """

    __tablename__ = "chat_messages"
    __table_args__ = (
        db.CheckConstraint(
            "sender IN ('user', 'ai')",
            name="ck_chat_messages_sender",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(
        db.Integer,
        db.ForeignKey("chat_rooms.id"),
        nullable=False,
        index=True,
    )
    sender = db.Column(db.String(10), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
        server_default=db.func.current_timestamp(),
        index=True,
    )

    room = db.relationship("ChatRoom", back_populates="messages", lazy="select")
