from flask_smorest import Blueprint


user_bp = Blueprint("users", __name__, description="User and pairing endpoints")

from app.users import routes  # noqa: E402, F401
