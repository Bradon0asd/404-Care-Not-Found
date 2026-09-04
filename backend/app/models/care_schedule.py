from enum import StrEnum

from app.extensions import db
from app.models.diary import utc_now


class ScheduleType(StrEnum):
    WEEKDAY = "weekday"
    WEEKEND = "weekend"


class CareSchedule(db.Model):
    __tablename__ = "care_schedules"
    __table_args__ = (
        db.CheckConstraint(
            "schedule_type IN ('weekday', 'weekend')",
            name="ck_care_schedules_schedule_type",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    care_recipient_id = db.Column(
        db.Integer,
        db.ForeignKey("care_recipients.id"),
        nullable=False,
        index=True,
    )
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    schedule_type = db.Column(db.String(20), nullable=False)
    weekday = db.Column(db.Integer, nullable=True)
    start_time = db.Column(db.Time, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
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

    care_recipient = db.relationship("CareRecipient", back_populates="schedules")
    creator = db.relationship("User", back_populates="created_schedules")
