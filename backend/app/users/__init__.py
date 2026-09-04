from flask import Blueprint



user_bp = Blueprint("users", __name__)

from app.users import routes  # noqa: E402, F401
