from flask_smorest import Blueprint


auth_bp = Blueprint("auth", __name__, description="Authentication endpoints")

from app.auth import routes  # noqa: E402, F401
