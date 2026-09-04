from flask_smorest import Blueprint

vital_sign_bp = Blueprint("vital_signs", __name__, description="Vital sign log endpoints")

from app.vital_signs import routes  # noqa: E402,F401
