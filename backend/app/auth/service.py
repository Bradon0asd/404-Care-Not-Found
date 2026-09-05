"""Authentication business logic backed by a server-side (filesystem) session."""

from datetime import datetime, timezone

from flask import session

from app.models import User
from app.shared.errors import AuthenticationError, UserNotFoundError
from app.users.service import get_user

SESSION_USER_ID = "user_id"
SESSION_ROLE = "role"
SESSION_LOGGED_IN_AT = "logged_in_at"


def login(*, line_id):
    """Start a session for the user owning this LINE id.

    The MVP identity is the LINE id alone; there is no password to verify yet.
    """
    user = User.query.filter_by(line_id=line_id).first()
    if user is None:
        raise AuthenticationError("Invalid credentials")

    # A fresh session id on login keeps a pre-login cookie from being reused.
    session.clear()
    session.permanent = True
    session[SESSION_USER_ID] = user.id
    session[SESSION_ROLE] = user.role
    session[SESSION_LOGGED_IN_AT] = datetime.now(timezone.utc).isoformat()
    return user


def logout():
    """Drop the server-side session. Safe to call when nobody is logged in."""
    session.clear()


def get_session_user():
    """Return the logged-in user, or None when the session is empty or stale."""
    user_id = session.get(SESSION_USER_ID)
    if user_id is None:
        return None

    try:
        return get_user(user_id=user_id)
    except UserNotFoundError:
        # The account was removed while the session file lived on.
        session.clear()
        return None


def require_session_user():
    user = get_session_user()
    if user is None:
        raise AuthenticationError("Login required")
    return user


def is_logged_in():
    return get_session_user() is not None
