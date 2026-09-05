from enum import StrEnum

from app.extensions import db
from app.models.diary import utc_now


class StressSource(StrEnum):
    CHAT = "chat"
    DIARY = "diary"


STRESS_SOURCES = tuple(source.value for source in StressSource)


class StressEvent(db.Model):
    """One high-stress signal, stored so the daily count can be aggregated.

    This model is the fourth pillar in table form: it records **that** something
    needs attention and **when**, and nothing else. There is deliberately no column
    for the caregiver's words, no excerpt, no summary, no reason, and no foreign key
    back to the diary or chat message that triggered it. The employer is told a
    count and a time; the content stays with her.

    Adding any content-bearing column here breaks that guarantee. Don't.
    """

    __tablename__ = "stress_events"
    __table_args__ = (
        db.CheckConstraint(
            "source IN ('chat', 'diary')",
            name="ck_stress_events_source",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    nurse_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    # Which path raised it, for engineering diagnostics only. Never pushed to LINE.
    source = db.Column(db.String(20), nullable=False)
    occurred_at = db.Column(db.DateTime, nullable=False, index=True)
    # Set once the day's aggregated push has gone out, so the same event is not
    # counted into a second notification (A3 throttling).
    notified_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
        server_default=db.func.current_timestamp(),
    )

    nurse = db.relationship("User", foreign_keys=[nurse_id], lazy="select")
