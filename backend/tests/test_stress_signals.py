import json

import pytest

from app.chat.client import GeminiClient
from app.extensions import db
from app.line.client import LineClient
from app.models import StressEvent, StressSource, User, UserRole
from app.models.diary import utc_now
from app.stress_signals import service


@pytest.fixture()
def line_app(app):
    app.config["LINE_CHANNEL_ACCESS_TOKEN"] = "test-access-token"
    app.config["GEMINI_API_KEY"] = "test-key"
    return app


@pytest.fixture()
def pushed_messages(monkeypatch):
    messages = []

    def fake_push_text(self, *, user_id, text):
        messages.append({"user_id": user_id, "text": text})

    monkeypatch.setattr(LineClient, "push_text", fake_push_text)
    return messages


@pytest.fixture()
def gemini(monkeypatch):
    """Queue up model replies and record which model each call used."""
    calls = []
    replies = []

    def fake_generate(self, prompt, *, system_instruction=None, temperature=0.7, json_mode=False):
        calls.append({"model": self.model, "prompt": prompt})
        if not replies:
            raise AssertionError("model called more times than the test queued replies")
        reply = replies.pop(0)
        if isinstance(reply, Exception):
            raise reply
        return json.dumps(reply)

    monkeypatch.setattr(GeminiClient, "generate_content", fake_generate)
    return {"calls": calls, "replies": replies}


def paired_nurse(app):
    owner = User(line_id="owner-line-id", role=UserRole.OWNER.value)
    nurse = User(line_id="nurse-line-id", role=UserRole.NURSE.value)
    db.session.add_all([owner, nurse])
    db.session.commit()
    owner.pair_user_id = nurse.id
    nurse.pair_user_id = owner.id
    db.session.commit()
    return nurse


def test_calm_message_stops_after_the_cheap_model(line_app, gemini, pushed_messages):
    """Tiered inference: a low triage score must not pay for the deep pass."""
    gemini["replies"].append({"score": 0.1})

    with line_app.app_context():
        nurse = paired_nurse(line_app)
        raised = service.analyze_and_record(
            nurse=nurse,
            text="Hari ini tenang.",
            source=StressSource.CHAT.value,
        )

        assert raised is False
        assert len(gemini["calls"]) == 1
        assert StressEvent.query.count() == 0
        assert pushed_messages == []


def test_high_stress_escalates_and_notifies_the_owner(line_app, gemini, pushed_messages):
    gemini["replies"].append({"score": 0.9})
    gemini["replies"].append({"score": 0.9, "high_stress": True, "reason": "self blame"})

    with line_app.app_context():
        nurse = paired_nurse(line_app)
        raised = service.analyze_and_record(
            nurse=nurse,
            text="Nenek jatuh dan aku merasa bersalah.",
            source=StressSource.CHAT.value,
        )

        assert raised is True
        assert len(gemini["calls"]) == 2
        assert StressEvent.query.count() == 1
        assert len(pushed_messages) == 1
        assert "異常筆數：1 筆" in pushed_messages[0]["text"]


def test_notice_never_carries_what_she_wrote(line_app, gemini, pushed_messages):
    """The fourth pillar: a count and a time leave the system, nothing else."""
    secret = "Nenek jatuh dan aku merasa bersalah sekali."
    gemini["replies"].append({"score": 0.9})
    gemini["replies"].append({"score": 0.95, "high_stress": True, "reason": secret})

    with line_app.app_context():
        nurse = paired_nurse(line_app)
        service.analyze_and_record(
            nurse=nurse,
            text=secret,
            source=StressSource.CHAT.value,
        )

        pushed = pushed_messages[0]["text"]
        assert secret not in pushed
        # Not even a fragment of it.
        for word in ("Nenek", "jatuh", "bersalah"):
            assert word not in pushed
        # And nothing was stored that could be joined back to her words.
        event = StressEvent.query.one()
        assert secret not in json.dumps(
            {c.name: str(getattr(event, c.name)) for c in StressEvent.__table__.columns}
        )


def test_second_event_the_same_day_pushes_the_running_total(line_app, gemini, pushed_messages):
    for _ in range(2):
        gemini["replies"].append({"score": 0.9})
        gemini["replies"].append({"score": 0.9, "high_stress": True})

    with line_app.app_context():
        nurse = paired_nurse(line_app)
        service.analyze_and_record(nurse=nurse, text="a", source=StressSource.CHAT.value)
        service.analyze_and_record(nurse=nurse, text="b", source=StressSource.DIARY.value)

        assert [
            "異常筆數：1 筆" in pushed_messages[0]["text"],
            "異常筆數：2 筆" in pushed_messages[1]["text"],
        ] == [True, True]


def test_an_already_notified_event_is_not_pushed_again(line_app, pushed_messages):
    """Re-running the aggregation must not re-notify a quiet day."""
    with line_app.app_context():
        nurse = paired_nurse(line_app)
        service.record_event(nurse=nurse, source=StressSource.CHAT.value)

        assert service.notify_daily_total(nurse=nurse) == 1
        assert service.notify_daily_total(nurse=nurse) is None
        assert len(pushed_messages) == 1


def test_failed_model_call_raises_no_signal(line_app, gemini, pushed_messages):
    """AI failure degrades to silence, never to a false alarm."""
    from app.shared.errors import GoogleAiApiError

    gemini["replies"].append(GoogleAiApiError("upstream down"))

    with line_app.app_context():
        nurse = paired_nurse(line_app)
        raised = service.analyze_and_record(
            nurse=nurse,
            text="apa saja",
            source=StressSource.CHAT.value,
        )

        assert raised is False
        assert StressEvent.query.count() == 0
        assert pushed_messages == []


def test_unpaired_nurse_keeps_the_event_for_the_next_push(line_app, pushed_messages):
    """A missing employer must not lose the signal or break the caller."""
    with line_app.app_context():
        nurse = User(line_id="lonely-nurse", role=UserRole.NURSE.value)
        db.session.add(nurse)
        db.session.commit()
        service.record_event(nurse=nurse, source=StressSource.CHAT.value)

        assert service.notify_daily_total(nurse=nurse) is None
        assert pushed_messages == []
        assert StressEvent.query.one().notified_at is None


def test_yesterdays_events_are_not_counted_into_today(line_app, pushed_messages):
    from datetime import timedelta

    with line_app.app_context():
        nurse = paired_nurse(line_app)
        service.record_event(
            nurse=nurse,
            source=StressSource.CHAT.value,
            occurred_at=utc_now() - timedelta(days=1),
        )
        service.record_event(nurse=nurse, source=StressSource.CHAT.value)

        assert service.notify_daily_total(nurse=nurse) == 1


def test_unknown_source_is_rejected(line_app):
    with line_app.app_context():
        nurse = paired_nurse(line_app)

        with pytest.raises(ValueError):
            service.record_event(nurse=nurse, source="employer")
