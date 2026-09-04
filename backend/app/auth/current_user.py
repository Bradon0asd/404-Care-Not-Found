from flask import request

from app.shared.errors import AuthenticationError
from app.users.service import get_user


def get_current_user():
    raw_user_id = request.headers.get("X-User-Id")
    if not raw_user_id:
        raise AuthenticationError("X-User-Id header is required")

    try:
        user_id = int(raw_user_id)
    except ValueError as error:
        raise AuthenticationError("X-User-Id must be an integer") from error

    return get_user(user_id=user_id)
