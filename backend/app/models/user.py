from enum import StrEnum

from app.extensions import db


class UserRole(StrEnum):
    OWNER = "owner"
    NURSE = "nurse"



class User(db.Model):
    __tablename__ = "users"
    __table_args__ = (
        db.CheckConstraint(
            "role IN ('owner', 'nurse')",
            name="ck_users_role",
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.String(128), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(10), nullable=True)
    role = db.Column(
        db.String(20),
        nullable=False,
        default=UserRole.NURSE.value,
        server_default=UserRole.NURSE.value,
    )
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        server_default=db.func.current_timestamp(),
    )
    owner_recipients = db.relationship(
        "CareRecipient",
        foreign_keys="CareRecipient.owner_id",
        back_populates="owner",
        lazy="select",
        passive_deletes=True,
    )
    nurse_recipients = db.relationship(
        "CareRecipient",
        foreign_keys="CareRecipient.nurse_id",
        back_populates="nurse",
        lazy="select",
        passive_deletes=True,
    )

    @property
    def care_recipients(self):
        if self.role == UserRole.NURSE.value:
            return self.nurse_recipients
        return self.owner_recipients


class CareRecipient(db.Model):
    __tablename__ = "care_recipients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="RESTRICT"),
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
        server_default=db.func.current_timestamp(),
    )
    owner = db.relationship(
        "User",
        foreign_keys=[owner_id],
        lazy="select",
        back_populates="owner_recipients",
    )
    nurse = db.relationship(
        "User",
        foreign_keys=[nurse_id],
        lazy="select",
        back_populates="nurse_recipients",
    )
