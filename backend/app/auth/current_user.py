from flask import request

from app.auth.service import require_session_user
from app.shared.errors import AuthenticationError
from app.users.service import get_user


def get_current_user():
    raw_user_id = request.headers.get("X-User-Id")
    if not raw_user_id:
        # The web app carries its identity in the session cookie; X-User-Id stays
        # for Swagger and scripts that have no cookie jar.
        return require_session_user()

    try:
        user_id = int(raw_user_id)
    except ValueError as error:
        raise AuthenticationError("X-User-Id must be an integer") from error

    return get_user(user_id=user_id)
