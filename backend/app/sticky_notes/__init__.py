from flask_smorest import Blueprint

sticky_note_bp = Blueprint("sticky_notes", __name__, description="Sticky note endpoints")

from app.sticky_notes import routes  # noqa: E402,F401
