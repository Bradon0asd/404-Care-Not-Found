from app.extensions import db
from app.models import CareSchedule
from app.shared.errors import CareScheduleNotFoundError
from app.shared.permissions import (
    get_accessible_care_recipient,
    require_care_recipient_access,
)


UPDATABLE_FIELDS = ("schedule_type", "weekday", "start_time", "title", "description")


def create_schedule(
    *,
    current_user,
    recipient_id,
    schedule_type,
    weekday,
    start_time,
    title,
    description=None,
):
    recipient = get_accessible_care_recipient(
        current_user=current_user,
        recipient_id=recipient_id,
    )
    schedule = CareSchedule(
        care_recipient_id=recipient.id,
        creator_id=current_user.id,
        schedule_type=schedule_type,
        weekday=weekday,
        start_time=start_time,
        title=title,
        description=description,
    )
    db.session.add(schedule)
    db.session.commit()
    return schedule


def list_schedules(*, current_user, recipient_id, schedule_type=None):
    recipient = get_accessible_care_recipient(
        current_user=current_user,
        recipient_id=recipient_id,
    )
    query = CareSchedule.query.filter(CareSchedule.care_recipient_id == recipient.id)

    if schedule_type is not None:
        query = query.filter(CareSchedule.schedule_type == schedule_type)

    return query.order_by(
        CareSchedule.weekday.asc(),
        CareSchedule.start_time.asc(),
        CareSchedule.id.asc(),
    ).all()


def get_schedule(*, current_user, schedule_id):
    schedule = db.session.get(CareSchedule, schedule_id)
    if schedule is None:
        raise CareScheduleNotFoundError("Care schedule not found")
    require_care_recipient_access(
        recipient=schedule.care_recipient,
        current_user=current_user,
    )
    return schedule


def update_schedule(*, current_user, schedule_id, **changes):
    schedule = get_schedule(current_user=current_user, schedule_id=schedule_id)

    for field in UPDATABLE_FIELDS:
        if field in changes:
            setattr(schedule, field, changes[field])
    db.session.commit()
    return schedule


def delete_schedule(*, current_user, schedule_id):
    schedule = get_schedule(current_user=current_user, schedule_id=schedule_id)
    db.session.delete(schedule)
    db.session.commit()
