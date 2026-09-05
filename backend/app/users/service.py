from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError

from app.shared.errors import UserAlreadyExistsError, UserNotFoundError, UserPairingError
from app.extensions import db
from app.models import User, UserRole


def create_user(*, line_id, name=None, language=None, role="nurse"):
    user = User(line_id=line_id, name=name, language=language, role=role)
    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise UserAlreadyExistsError("User already exists") from error
    return user


def get_user(*, user_id):
    user = db.session.get(User, user_id)
    if user is None:
        raise UserNotFoundError("User not found")
    return user


def complete_onboarding(*, user, name=None, language=None):
    """Finish the one-off setup form. The stamp is what later logins are judged on."""
    if name is not None:
        user.name = name
    if language is not None:
        user.language = language
    # Re-running the form must not move the stamp, or "already registered" would drift.
    if user.onboarded_at is None:
        user.onboarded_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.session.commit()
    return user


def get_or_create_user(*, line_id, name=None, role=UserRole.NURSE.value):
    user = User.query.filter_by(line_id=line_id).first()
    if user is not None:
        return user
    return create_user(line_id=line_id, name=name, role=role)


def pair_users(user, target_user):
    if user.id == target_user.id:
        raise UserPairingError("Cannot pair user with itself")

    owner, nurse = _normalize_pair(user, target_user)

    if owner.pair_user_id is not None:
        raise UserPairingError("Owner already paired")

    if nurse.pair_user_id is not None:
        raise UserPairingError("Nurse already paired")

    owner.pair_user_id = nurse.id
    nurse.pair_user_id = owner.id

    try:
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        raise UserPairingError("User pairing violates uniqueness constraints") from error

    return user


def unpair_users(user):
    paired_user = user.paired_user

    if paired_user is None:
        return user

    user.pair_user_id = None

    if paired_user.pair_user_id == user.id:
        paired_user.pair_user_id = None

    db.session.commit()
    return user


def _normalize_pair(first_user, second_user):
    roles = {first_user.role, second_user.role}
    expected_roles = {UserRole.OWNER.value, UserRole.NURSE.value}
    if roles != expected_roles:
        raise UserPairingError("Owner and nurse roles are required")

    if first_user.role == UserRole.OWNER.value:
        return first_user, second_user

    return second_user, first_user
