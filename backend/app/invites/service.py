import secrets

from flask import current_app

from app.auth.service import start_session
from app.extensions import db
from app.models import Invite, User, UserRole
from app.models.invite import generate_code
from app.shared.errors import (
    InviteNotFoundError,
    InviteRevokedError,
    PermissionDeniedError,
)


INVITE_PATH = "/auth/role?invite={code}"
WEB_LINE_ID_PREFIX = "web-"


def create_invite(*, owner):
    """Return the owner's active invite, creating one on first request."""
    if owner.role != UserRole.OWNER.value:
        raise PermissionDeniedError("Only an owner can invite a caregiver")

    invite = active_invite_for(owner=owner)
    if invite is not None:
        return invite

    invite = Invite(code=generate_code(), owner_id=owner.id)
    db.session.add(invite)
    db.session.commit()
    return invite


def active_invite_for(*, owner):
    return (
        Invite.query.filter(Invite.owner_id == owner.id, Invite.revoked_at.is_(None))
        .order_by(Invite.id.desc())
        .first()
    )


def get_invite(*, code):
    invite = Invite.query.filter_by(code=code).first()
    if invite is None:
        raise InviteNotFoundError("Invite not found")
    if not invite.is_active:
        raise InviteRevokedError("Invite is no longer valid")
    return invite


def enter_invite(*, code):
    """Turn the link into a signed-in caregiver. No registration, no password."""
    invite = get_invite(code=code)
    nurse = invite.nurse or _bind_nurse(invite)
    start_session(nurse)
    return nurse


def complete_profile(*, code, name, language=None):
    invite = get_invite(code=code)
    nurse = invite.nurse or _bind_nurse(invite)
    nurse.name = name
    if language is not None:
        nurse.language = language
    db.session.commit()
    start_session(nurse)
    return nurse


def needs_profile(nurse):
    return not nurse.name


def build_invite_url(invite):
    base = current_app.config.get("WEB_APP_BASE_URL", "").rstrip("/")
    path = INVITE_PATH.format(code=invite.code)
    return f"{base}{path}" if base else path


def _bind_nurse(invite):
    """Attach a caregiver to the invite, reusing an existing pairing if there is one."""
    owner = invite.owner
    paired = owner.paired_user

    if paired is not None and paired.role == UserRole.NURSE.value:
        nurse = paired
    else:
        nurse = User(
            # Web caregivers never touch LINE, but line_id is required and unique.
            line_id=f"{WEB_LINE_ID_PREFIX}{secrets.token_urlsafe(24)}",
            role=UserRole.NURSE.value,
        )
        db.session.add(nurse)
        db.session.commit()
        owner.pair_user_id = nurse.id
        nurse.pair_user_id = owner.id

    invite.nurse_id = nurse.id
    db.session.commit()
    return nurse
