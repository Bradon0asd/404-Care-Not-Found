from flask_smorest import Blueprint

chat_bp = Blueprint("chat", __name__, description="Care agent and tree hollow chat operations")

from app.chat import routes  # noqa: E402,F401
