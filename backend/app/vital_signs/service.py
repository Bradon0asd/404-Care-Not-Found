from datetime import datetime, time, timezone

from app.extensions import db
from app.models import VITAL_SIGN_UNITS, VitalSignLog
from app.shared.permissions import get_accessible_care_recipient


def create_vital_sign(
    *,
    current_user,
    recipient_id,
    vital_type,
    value,
    measured_at,
    secondary_value=None,
    note=None,
):
    recipient = get_accessible_care_recipient(
        current_user=current_user,
        recipient_id=recipient_id,
    )
    log = VitalSignLog(
        care_recipient_id=recipient.id,
        creator_id=current_user.id,
        vital_type=vital_type,
        value=value,
        secondary_value=secondary_value,
        # The unit is derived from the type, never taken from the client.
        unit=VITAL_SIGN_UNITS[vital_type],
        measured_at=to_naive_utc(measured_at),
        note=note,
    )
    db.session.add(log)
    db.session.commit()
    return log


def list_vital_signs(
    *,
    current_user,
    recipient_id,
    vital_type=None,
    start_date=None,
    end_date=None,
):
    recipient = get_accessible_care_recipient(
        current_user=current_user,
        recipient_id=recipient_id,
    )
    query = VitalSignLog.query.filter(VitalSignLog.care_recipient_id == recipient.id)

    if vital_type is not None:
        query = query.filter(VitalSignLog.vital_type == vital_type)
    if start_date is not None:
        query = query.filter(VitalSignLog.measured_at >= datetime.combine(start_date, time.min))
    if end_date is not None:
        query = query.filter(VitalSignLog.measured_at <= datetime.combine(end_date, time.max))

    return query.order_by(
        VitalSignLog.measured_at.desc(),
        VitalSignLog.id.desc(),
    ).all()


def to_naive_utc(value):
    """Store every timestamp as naive UTC so period comparisons stay consistent."""
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)
