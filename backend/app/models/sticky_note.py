from enum import StrEnum

from app.extensions import db
from app.models.diary import utc_now


class StickyNotePriority(StrEnum):
    URGENT = "urgent"
    NORMAL = "normal"
    LOW = "low"


class StickyNoteCategory(StrEnum):
    LEAVE = "leave"
    FAMILY = "family"
    CARE = "care"
    SHOPPING = "shopping"
    OTHER = "other"


class StickyNote(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(30), nullable=True)
    priority = db.Column(
        db.String(20),
        nullable=False,
        default=StickyNotePriority.NORMAL.value,
        server_default=StickyNotePriority.NORMAL.value,
    )
    images = db.Column(
        db.JSON,
        nullable=False,
        default=list,
    )
    is_reviewed = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default=db.false(),
    )
    is_private = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
        server_default=db.false(),
    )
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

    creator = db.relationship("User", back_populates="sticky_notes")
