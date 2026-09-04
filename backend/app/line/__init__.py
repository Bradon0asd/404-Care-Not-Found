from flask_smorest import Blueprint


line_bp = Blueprint("line", __name__, description="LINE webhook endpoints")

from app.line import routes  # noqa: E402, F401
