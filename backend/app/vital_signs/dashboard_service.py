from datetime import datetime, time, timedelta, timezone

from sqlalchemy import func

from app.extensions import db
from app.models import VITAL_SIGN_UNITS, VitalSignLog, VitalSignType
from app.shared.permissions import get_accessible_care_recipient


PERIOD_DAYS = 7
SECONDARY_LABELS = {
    VitalSignType.BLOOD_PRESSURE.value: ("\u6536\u7e2e\u58d3", "\u8212\u5f35\u58d3"),
}


def build_dashboard(*, current_user, recipient_id, reference=None):
    """Aggregate existing logs only. No diagnosis, no medical advice."""
    recipient = get_accessible_care_recipient(
        current_user=current_user,
        recipient_id=recipient_id,
    )
    period = build_periods(reference or _utc_now())
    current_averages = _averages(recipient.id, period["current_start"], period["current_end"])
    previous_averages = _averages(recipient.id, period["previous_start"], period["previous_end"])

    dashboard = {"period": period}
    for vital_type in VitalSignType:
        dashboard[vital_type.value] = _build_metric(
            recipient_id=recipient.id,
            vital_type=vital_type.value,
            current_average=current_averages.get(vital_type.value),
            previous_average=previous_averages.get(vital_type.value),
        )
    return dashboard


def build_periods(reference):
    # Day-aligned windows: the current period ends at the start of tomorrow.
    current_end = datetime.combine(reference.date() + timedelta(days=1), time.min)
    current_start = current_end - timedelta(days=PERIOD_DAYS)
    previous_end = current_start
    previous_start = previous_end - timedelta(days=PERIOD_DAYS)
    return {
        "current_start": current_start,
        "current_end": current_end,
        "previous_start": previous_start,
        "previous_end": previous_end,
    }


def _build_metric(*, recipient_id, vital_type, current_average, previous_average):
    difference = _difference(current_average, previous_average)
    return {
        "unit": VITAL_SIGN_UNITS[vital_type],
        "latest": _latest(recipient_id, vital_type),
        "current_average": current_average,
        "previous_average": previous_average,
        "difference": difference,
        "change_text": _build_change_text(vital_type, difference),
    }


def _latest(recipient_id, vital_type):
    log = (
        VitalSignLog.query.filter(
            VitalSignLog.care_recipient_id == recipient_id,
            VitalSignLog.vital_type == vital_type,
        )
        .order_by(VitalSignLog.measured_at.desc(), VitalSignLog.id.desc())
        .first()
    )
    if log is None:
        return None
    return {
        "value": log.value,
        "secondary_value": log.secondary_value,
        "measured_at": log.measured_at,
    }


def _averages(recipient_id, start, end):
    rows = (
        db.session.query(
            VitalSignLog.vital_type,
            func.avg(VitalSignLog.value),
            func.avg(VitalSignLog.secondary_value),
        )
        .filter(
            VitalSignLog.care_recipient_id == recipient_id,
            VitalSignLog.measured_at >= start,
            VitalSignLog.measured_at < end,
        )
        .group_by(VitalSignLog.vital_type)
        .all()
    )
    return {
        vital_type: {"value": _round(value), "secondary_value": _round(secondary_value)}
        for vital_type, value, secondary_value in rows
    }


def _difference(current_average, previous_average):
    if current_average is None or previous_average is None:
        return None
    return {
        "value": _subtract(current_average["value"], previous_average["value"]),
        "secondary_value": _subtract(
            current_average["secondary_value"],
            previous_average["secondary_value"],
        ),
    }


def _build_change_text(vital_type, difference):
    if difference is None:
        return None

    labels = SECONDARY_LABELS.get(vital_type)
    if labels is None:
        return _describe(difference["value"])

    parts = []
    for label, key in zip(labels, ("value", "secondary_value")):
        described = _describe(difference[key])
        if described is not None:
            parts.append(f"{label}{described}")
    return "\uff0c".join(parts) or None


def _describe(difference):
    # Only increase / decrease / same. Never healthy, dangerous or abnormal.
    if difference is None:
        return None
    if difference > 0:
        return f"\u8f03\u524d\u671f\u589e\u52a0 {_format(difference)}"
    if difference < 0:
        return f"\u8f03\u524d\u671f\u6e1b\u5c11 {_format(abs(difference))}"
    return "\u8207\u524d\u671f\u76f8\u540c"


def _subtract(current, previous):
    if current is None or previous is None:
        return None
    return _round(current - previous)


def _round(value):
    if value is None:
        return None
    return round(float(value), 1) + 0.0


def _format(value):
    if float(value).is_integer():
        return str(int(value))
    return str(value)


def _utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)
