from flask_smorest import Blueprint

invite_bp = Blueprint("invites", __name__, description="Caregiver invite links")

from app.invites import routes  # noqa: E402,F401
