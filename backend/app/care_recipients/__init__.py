from flask_smorest import Blueprint

care_recipient_bp = Blueprint("care_recipients", __name__, description="Care recipient endpoints")

from app.care_recipients import routes  # noqa: E402,F401
