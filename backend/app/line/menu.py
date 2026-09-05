from datetime import datetime, timezone

from app.care_schedules.service import list_schedules
from app.invites.service import build_invite_url, create_invite
from app.models import ScheduleType, StickyNotePriority, VitalSignType
from app.sticky_notes.service import list_notes
from app.vital_signs.dashboard_service import build_dashboard


VITAL_SIGN_LABELS = {
    VitalSignType.BLOOD_PRESSURE.value: "血壓",
    VitalSignType.BLOOD_GLUCOSE.value: "血糖",
    VitalSignType.HEART_RATE.value: "心跳",
    VitalSignType.OXYGEN_SATURATION.value: "血氧",
    VitalSignType.TEMPERATURE.value: "體溫",
    VitalSignType.RESPIRATORY_RATE.value: "呼吸",
}

PRIORITY_LABELS = {
    StickyNotePriority.URGENT.value: "緊急",
    StickyNotePriority.NORMAL.value: "普通",
    StickyNotePriority.LOW.value: "不重要",
}

NOTE_LIMIT = 5
NOTE_CONTENT_LIMIT = 40

HELP_REPLY = "\n".join(
    [
        "可以點選下方選單：",
        "・照護摘要推播",
        "・交流版便利貼",
    ]
)

STRESS_NOTICE_REPLY = "\n".join(
    [
        "壓力告知會在需要時自動送達，不需要查詢。",
        "",
        "通知只會包含需要留意的紀錄筆數、時間，以及建議的關心方式。",
        "看護寫下的內容屬於她自己，不會出現在通知裡。",
    ]
)


def build_menu_reply(*, user, text):
    """Return the reply for a menu tap, or None when the text is not a menu item."""
    handler = MENU_HANDLERS.get(text.strip())
    if handler is None:
        return None
    return handler(user)


def _care_summary_reply(user):
    recipient = _first_care_recipient(user)
    if recipient is None:
        return "還沒有被照護者的資料，請先在系統中建立。"

    lines = [f"照護摘要（{recipient.name}）", ""]
    lines.extend(_vital_sign_lines(user, recipient))
    lines.append("")
    lines.extend(_schedule_lines(user, recipient))
    return "\n".join(lines)


def _sticky_notes_reply(user):
    notes = list_notes(current_user=user)[:NOTE_LIMIT]
    if not notes:
        return "交流板目前沒有新的便利貼。"

    lines = ["交流板"]
    for note in notes:
        priority = PRIORITY_LABELS.get(note.priority, note.priority)
        lines.append("")
        lines.append(f"【{priority}】{note.title}")
        lines.append(f"{note.created_at:%m/%d}　{_shorten(note.content)}")
    return "\n".join(lines)


def _invite_reply(user):
    invite = create_invite(owner=user)
    return "\n".join(
        [
            "邀請看護加入",
            "",
            "把這條連結傳給看護，她點開填好基本資料就能直接開始使用，不需要註冊或密碼：",
            build_invite_url(invite),
            "",
            "同一條連結可以重複使用，她每次點開都會回到自己的紀錄。",
        ]
    )


def _stress_notice_reply(user):
    return STRESS_NOTICE_REPLY


def _vital_sign_lines(user, recipient):
    dashboard = build_dashboard(current_user=user, recipient_id=recipient.id)

    lines = ["生命徵象"]
    for vital_type in VitalSignType:
        metric = dashboard[vital_type.value]
        if metric["latest"] is None:
            continue
        lines.append(
            f"・{VITAL_SIGN_LABELS[vital_type.value]} "
            f"{_format_reading(metric)}{_format_change(metric)}"
        )

    if len(lines) == 1:
        lines.append("・目前還沒有紀錄")
    return lines


def _schedule_lines(user, recipient):
    today = _today()
    schedules = [
        schedule
        for schedule in list_schedules(
            current_user=user,
            recipient_id=recipient.id,
            schedule_type=_schedule_type(today),
        )
        if schedule.weekday in (None, today.weekday())
    ]

    if not schedules:
        return ["今日排程", "・目前還沒有安排"]

    lines = [f"今日排程 {len(schedules)} 項"]
    lines.extend(f"・{schedule.start_time:%H:%M}　{schedule.title}" for schedule in schedules)
    return lines


def _format_reading(metric):
    latest = metric["latest"]
    value = _format_number(latest["value"])
    if latest["secondary_value"] is not None:
        value = f"{value}/{_format_number(latest['secondary_value'])}"
    return f"{value} {metric['unit']}"


def _format_change(metric):
    change_text = metric["change_text"]
    if change_text is None:
        return ""
    return f"（{change_text}）"


def _format_number(value):
    if value is None:
        return "-"
    if float(value).is_integer():
        return str(int(value))
    return str(round(float(value), 1))


def _first_care_recipient(user):
    recipients = user.care_recipients
    if not recipients:
        return None
    return recipients[0]


def _schedule_type(reference):
    if reference.weekday() >= 5:
        return ScheduleType.WEEKEND.value
    return ScheduleType.WEEKDAY.value


def _today():
    return datetime.now(timezone.utc).replace(tzinfo=None)


MENU_HANDLERS = {
    "照護摘要推播": _care_summary_reply,
    "照護摘要": _care_summary_reply,
    "交流版便利貼": _sticky_notes_reply,
    "交流板便利貼": _sticky_notes_reply,
    "交流板": _sticky_notes_reply,
    "壓力告知": _stress_notice_reply,
    "邀請看護": _invite_reply,
    "邀請": _invite_reply,
}


def _shorten(content):
    collapsed = " ".join(content.split())
    if len(collapsed) <= NOTE_CONTENT_LIMIT:
        return collapsed
    return collapsed[:NOTE_CONTENT_LIMIT] + "…"
