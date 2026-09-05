from flask import Blueprint as FlaskBlueprint
from flask_smorest import Blueprint

upload_bp = Blueprint("uploads", __name__, description="Image upload endpoints")
media_bp = FlaskBlueprint("media", __name__)

from app.uploads import routes  # noqa: E402,F401
