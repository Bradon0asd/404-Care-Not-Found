"""Authentication business logic backed by a server-side (filesystem) session."""

import logging
import secrets
from datetime import datetime, timezone
from urllib.parse import urlencode

from flask import current_app, session

from app.auth.line_client import LineLoginClient
from app.extensions import db
from app.models import User, UserRole
from app.shared.errors import (
    AuthenticationError,
    LineLoginError,
    RoleMismatchError,
    UserNotFoundError,
)
from app.users.service import get_user

logger = logging.getLogger(__name__)

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

    return start_session(user)


def start_session(user):
    """Put a user into the session. Shared by the LINE id login and LINE Login."""
    # A fresh session id keeps a pre-login cookie from being reused.
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


# --- LINE Login (SSO) -------------------------------------------------------

STATE_KEY_PREFIX = "line_login_state:"
DEFAULT_STATE_TTL_SECONDS = 600


def start_line_login(*, role, client=None):
    """Stash the selected role behind a fresh OAuth state and return the LINE URL."""
    client = client or LineLoginClient()
    state = secrets.token_urlsafe(32)
    _state_store().set(f"{STATE_KEY_PREFIX}{state}", {"role": role}, timeout=_state_ttl())
    return client.build_authorization_url(state=state)


def consume_login_state(state):
    """Return the role bound to this state, and burn the state so it cannot repeat."""
    if not state:
        raise LineLoginError("Missing OAuth state")

    key = f"{STATE_KEY_PREFIX}{state}"
    store = _state_store()
    stored = store.get(key)
    # Deleted before any further work, so a replayed callback finds nothing.
    store.delete(key)
    if not stored:
        raise LineLoginError("OAuth state is unknown or expired")
    return stored["role"]


def complete_line_login(*, code, state, client=None):
    """Finish the callback: verify the LINE identity, resolve the user, open a session."""
    if not code:
        raise LineLoginError("Missing authorization code")

    selected_role = consume_login_state(state)
    client = client or LineLoginClient()
    line_id, display_name = client.fetch_identity(code=code)
    if not line_id:
        raise LineLoginError("LINE identity carried no user id")

    user = resolve_line_user(
        line_id=line_id,
        display_name=display_name,
        selected_role=selected_role,
    )
    return start_session(user)


def resolve_line_user(*, line_id, display_name, selected_role):
    """First login creates the user with the selected role; later logins never rewrite it."""
    user = User.query.filter_by(line_id=line_id).first()
    if user is not None:
        if user.role != selected_role:
            raise RoleMismatchError("The selected role does not match this account.")
        return user

    user = User(line_id=line_id, name=display_name, role=UserRole(selected_role).value)
    db.session.add(user)
    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("line login could not create the user")
        raise
    return user


def frontend_redirect_url(*, path_config_key, default_path, params=None):
    """Build the URL the callback sends the browser back to."""
    base = (current_app.config.get("FRONTEND_URL") or "http://localhost:5173").rstrip("/")
    path = current_app.config.get(path_config_key) or default_path
    if not path.startswith("/"):
        path = f"/{path}"
    url = f"{base}{path}"
    if params:
        url = f"{url}?{urlencode(params)}"
    return url


def _state_store():
    # Reuses the session cache, so state survives across gunicorn workers.
    return current_app.config["SESSION_CACHELIB"]


def _state_ttl():
    return int(current_app.config.get("LINE_LOGIN_STATE_TTL", DEFAULT_STATE_TTL_SECONDS))
