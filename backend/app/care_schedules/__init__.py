from flask_smorest import Blueprint

care_schedule_bp = Blueprint("care_schedules", __name__, description="Care schedule endpoints")

from app.care_schedules import routes  # noqa: E402,F401
