"""Session guards for API views.

Not applied to any route yet; wire them in once the frontend sends the session
cookie instead of the X-User-Id header.
"""

from functools import wraps

from flask import g

from app.auth.service import require_session_user
from app.shared.errors import PermissionDeniedError


def login_required(view):
    """Reject the request unless a session user exists, and expose it as g.current_user."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        g.current_user = require_session_user()
        return view(*args, **kwargs)

    return wrapper


def role_required(*roles):
    """Reject the request unless the session user holds one of these roles."""
    allowed = {str(role) for role in roles}

    def decorator(view):
        @wraps(view)
        @login_required
        def wrapper(*args, **kwargs):
            if g.current_user.role not in allowed:
                raise PermissionDeniedError(f"Requires role: {', '.join(sorted(allowed))}")
            return view(*args, **kwargs)

        return wrapper

    return decorator
