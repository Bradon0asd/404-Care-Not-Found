from enum import StrEnum

from app.extensions import db
from datetime import datetime, timezone


class StickyNotePriority(StrEnum):
    URGENT = "urgent"
    NORMAL = "normal"
    LOW = "low"


class StickyNote(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)

    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )

    title = db.Column(
        db.String(100),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )

    # leave / family / care / shopping / other
    category = db.Column(
        db.String(30),
        nullable=True,
    )

    # urgent / normal / low
    priority = db.Column(
        db.String(20),
        nullable=False,
        default=StickyNotePriority.NORMAL.value,
    )

    is_reviewed = db.Column(
        db.Boolean,
        default=False,
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    creator = db.relationship(
        "User", back_populates="sticky_notes", foreign_keys=[creator_id]
    )


class DiaryEntry(db.Model):
    __tablename__ = "diary_entries"

    id = db.Column(db.Integer, primary_key=True)

    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
    )
    


    title = db.Column(
        db.String(100),
        nullable=False,
    )

    content = db.Column(
        db.Text,
        nullable=False,
    )
    
    
    images = db.Column(
        db.JSON,
        nullable=False,
        default=list,
    )
    
    is_private = db.Column(
        db.Boolean,
        default=True,
    )
    
    #if is_private is True
    #Ai will analyze the content
    ai_analysis = db.Column(
        db.String(64),
        nullable=True,
    )

    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    creator = db.relationship(
        "User", back_populates="diary_entries", foreign_keys=[creator_id]
    )
