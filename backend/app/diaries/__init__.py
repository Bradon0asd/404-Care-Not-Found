from flask_smorest import Blueprint

diary_bp = Blueprint("diaries", __name__, description="Diary endpoints")

from app.diaries import routes  # noqa: E402,F401
