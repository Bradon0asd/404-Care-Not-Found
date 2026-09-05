import secrets

from app.extensions import db
from app.models.diary import utc_now


CODE_BYTES = 24


def generate_code():
    """A link is the caregiver's only credential, so make it unguessable."""
    return secrets.token_urlsafe(CODE_BYTES)


class Invite(db.Model):
    __tablename__ = "invites"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False, index=True)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    nurse_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
        server_default=db.func.current_timestamp(),
    )
    revoked_at = db.Column(db.DateTime, nullable=True)

    owner = db.relationship("User", foreign_keys=[owner_id])
    nurse = db.relationship("User", foreign_keys=[nurse_id])

    @property
    def is_active(self):
        return self.revoked_at is None
