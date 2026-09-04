from flask import Blueprint


line_bp = Blueprint("line", __name__)

from app.line import routes  # noqa: E402, F401
