"""Authentication guards for API views."""

from functools import wraps

from flask import g

from app.shared.errors import PermissionDeniedError


def login_required(view):
    """Reject unless the request has a session user or X-User-Id fallback."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        # Imported lazily to avoid a module cycle: current_user imports auth.service,
        # and auth.service imports users.service.
        from app.auth.current_user import get_current_user

        g.current_user = get_current_user()
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
