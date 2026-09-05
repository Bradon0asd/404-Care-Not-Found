from datetime import datetime, timezone

from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class Diary(db.Model):
    __tablename__ = "diaries"

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    title = db.Column(db.String(100), nullable=True)
    content = db.Column(db.Text, nullable=False)
    # One image per diary entry, stored as a URL; the file itself never enters the DB.
    image_url = db.Column(db.String(500), nullable=True)
    is_private = db.Column(
        db.Boolean,
        nullable=False,
        default=True,
        server_default=db.true(),
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

    creator = db.relationship("User", back_populates="diaries")
