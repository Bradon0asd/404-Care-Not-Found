import pytest
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import (
    CareAgent,
    CareRecipient,
    ChatMessage,
    ChatRoom,
    MessageSender,
    MoodWeather,
    StressEvent,
    StressSource,
    User,
    UserRole,
)
from app.models.diary import utc_now


def build_agent():
    owner = User(line_id="owner-line-id", role=UserRole.OWNER.value)
    nurse = User(line_id="nurse-line-id", role=UserRole.NURSE.value)
    recipient = CareRecipient(name="Patient", owner=owner, nurse=nurse)
    agent = CareAgent(
        user=nurse,
        care_recipient=recipient,
        system_prompt="Merawat nenek berusia 90 tahun.",
    )
    db.session.add(agent)
    db.session.commit()
    return agent


def test_agent_defaults_to_unfinished_setup(app):
    with app.app_context():
        agent = build_agent()

        assert agent.temperature == 0.7
        # No baseline yet, so Tab 03 still shows the one-off setup flow.
        assert agent.baseline_completed_at is None
        assert agent.generated_profile is None


def test_room_and_messages_hang_off_the_agent(app):
    with app.app_context():
        agent = build_agent()
        room = ChatRoom(
            user_id=agent.user_id,
            care_agent=agent,
            title="Nenek jatuh",
            mood_weather=MoodWeather.RAINY.value,
        )
        room.messages.append(ChatMessage(sender=MessageSender.USER.value, text="Aku sedih."))
        room.messages.append(ChatMessage(sender=MessageSender.AI.value, text="Aku di sini."))
        db.session.add(room)
        db.session.commit()

        assert agent.rooms == [room]
        assert [message.sender for message in room.messages] == ["user", "ai"]


def test_deleting_a_room_takes_its_messages(app):
    with app.app_context():
        agent = build_agent()
        room = ChatRoom(user_id=agent.user_id, care_agent=agent)
        room.messages.append(ChatMessage(sender=MessageSender.USER.value, text="Halo."))
        db.session.add(room)
        db.session.commit()

        db.session.delete(room)
        db.session.commit()

        assert ChatMessage.query.count() == 0


def test_message_carries_no_stress_column(app):
    """The caregiver's words and any stress reading must never share a row."""
    columns = {column.name for column in ChatMessage.__table__.columns}

    assert columns == {"id", "room_id", "sender", "text", "created_at"}


def test_stress_event_stores_a_signal_and_nothing_she_wrote(app):
    """The fourth pillar in table form: a count and a time, never the content."""
    columns = {column.name for column in StressEvent.__table__.columns}

    assert columns == {
        "id",
        "nurse_id",
        "source",
        "occurred_at",
        "notified_at",
        "created_at",
    }
    # The only link out points at the nurse. Nothing ties a signal back to the diary
    # or message that raised it, and no column is free text.
    referenced_tables = {
        key.column.table.name
        for column in StressEvent.__table__.columns
        for key in column.foreign_keys
    }
    assert referenced_tables == {"users"}
    assert not [
        column for column in StressEvent.__table__.columns
        if isinstance(column.type, db.Text)
    ]


def test_stress_event_starts_unnotified(app):
    with app.app_context():
        nurse = User(line_id="nurse-line-id", role=UserRole.NURSE.value)
        db.session.add(nurse)
        db.session.commit()
        event = StressEvent(
            nurse_id=nurse.id,
            source=StressSource.CHAT.value,
            occurred_at=utc_now(),
        )
        db.session.add(event)
        db.session.commit()

        # Only aggregated pushes set this, so the same event is never counted twice.
        assert event.notified_at is None


def test_mood_weather_rejects_a_value_outside_the_four(app):
    with app.app_context():
        agent = build_agent()
        db.session.add(
            ChatRoom(user_id=agent.user_id, care_agent=agent, mood_weather="tornado")
        )

        with pytest.raises(IntegrityError):
            db.session.commit()
