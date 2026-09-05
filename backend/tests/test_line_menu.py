from datetime import datetime, time, timedelta, timezone

import pytest

from app.extensions import db
from app.line.menu import build_menu_reply
from app.models import (
    CareRecipient,
    CareSchedule,
    ScheduleType,
    StickyNote,
    User,
    UserRole,
    VitalSignLog,
)


@pytest.fixture()
def owner(app):
    with app.app_context():
        owner = User(line_id="owner-line-id", role=UserRole.OWNER.value)
        nurse = User(line_id="nurse-line-id", role=UserRole.NURSE.value)
        db.session.add_all([owner, nurse])
        db.session.commit()

        owner.pair_user_id = nurse.id
        nurse.pair_user_id = owner.id
        db.session.commit()
        yield owner


def test_unknown_text_is_not_a_menu_item(app, owner):
    with app.app_context():
        assert build_menu_reply(user=owner, text="halo") is None


def test_care_summary_without_a_care_recipient(app, owner):
    with app.app_context():
        reply = build_menu_reply(user=owner, text="照護摘要推播")

        assert reply == "還沒有被照護者的資料，請先在系統中建立。"


def test_care_summary_reports_readings_and_schedule(app, owner):
    with app.app_context():
        recipient = _care_recipient(owner)
        _add_vital_sign(recipient, owner, "heart_rate", 78.0, days_ago=1)
        _add_schedule(recipient, owner, time(8, 0), "平日早餐", ScheduleType.WEEKDAY.value)
        _add_schedule(recipient, owner, time(9, 0), "週末早餐", ScheduleType.WEEKEND.value)
        db.session.commit()

        reply = build_menu_reply(user=owner, text="照護摘要推播")

        assert "照護摘要（阿嬤）" in reply
        assert "・心跳 78 bpm" in reply

        # Only the schedule matching today's kind of day is offered.
        if _now().weekday() >= 5:
            shown, hidden, shown_at = "週末早餐", "平日早餐", "09:00"
        else:
            shown, hidden, shown_at = "平日早餐", "週末早餐", "08:00"
        assert shown in reply
        assert shown_at in reply
        assert hidden not in reply


def test_care_summary_never_labels_a_reading_as_abnormal(app, owner):
    with app.app_context():
        recipient = _care_recipient(owner)
        _add_vital_sign(recipient, owner, "heart_rate", 130.0, days_ago=1)
        db.session.commit()

        reply = build_menu_reply(user=owner, text="照護摘要推播")

        for forbidden in ("異常", "偏高", "危險", "警告", "正常"):
            assert forbidden not in reply


def test_care_summary_without_records(app, owner):
    with app.app_context():
        _care_recipient(owner)
        db.session.commit()

        reply = build_menu_reply(user=owner, text="照護摘要推播")

        assert "・目前還沒有紀錄" in reply
        assert "・目前還沒有安排" in reply


def test_sticky_notes_without_any_note(app, owner):
    with app.app_context():
        reply = build_menu_reply(user=owner, text="交流版便利貼")

        assert reply == "交流板目前沒有新的便利貼。"


def test_sticky_notes_list_shared_notes_by_priority_label(app, owner):
    with app.app_context():
        _add_note(owner.paired_user, title="臨時請假", content="下週三想請一天假", priority="urgent")
        db.session.commit()

        reply = build_menu_reply(user=owner, text="交流版便利貼")

        assert "【緊急】臨時請假" in reply
        assert "下週三想請一天假" in reply


def test_sticky_notes_hide_private_notes(app, owner):
    with app.app_context():
        _add_note(owner.paired_user, title="私人筆記", content="不給雇主看", is_private=True)
        db.session.commit()

        reply = build_menu_reply(user=owner, text="交流版便利貼")

        assert "私人筆記" not in reply
        assert "不給雇主看" not in reply


def test_stress_notice_explains_it_arrives_automatically(app, owner):
    with app.app_context():
        _add_note(owner.paired_user, title="私人筆記", content="不給雇主看", is_private=True)
        db.session.commit()

        reply = build_menu_reply(user=owner, text="壓力告知")

        assert "自動送達" in reply
        assert "不給雇主看" not in reply


def _care_recipient(owner):
    recipient = CareRecipient(
        name="阿嬤",
        owner_id=owner.id,
        nurse_id=owner.pair_user_id,
    )
    db.session.add(recipient)
    db.session.commit()
    return recipient


def _add_vital_sign(recipient, creator, vital_type, value, *, days_ago):
    db.session.add(
        VitalSignLog(
            care_recipient_id=recipient.id,
            creator_id=creator.id,
            vital_type=vital_type,
            value=value,
            unit="bpm",
            measured_at=_now() - timedelta(days=days_ago),
        )
    )


def _add_schedule(recipient, creator, start_time, title, schedule_type):
    db.session.add(
        CareSchedule(
            care_recipient_id=recipient.id,
            creator_id=creator.id,
            schedule_type=schedule_type,
            weekday=None,
            start_time=start_time,
            title=title,
        )
    )


def _add_note(creator, *, title, content, priority="normal", is_private=False):
    db.session.add(
        StickyNote(
            creator_id=creator.id,
            title=title,
            content=content,
            priority=priority,
            images=[],
            is_private=is_private,
            is_reviewed=False,
        )
    )


def _now():
    return datetime.now(timezone.utc).replace(tzinfo=None)
