from flask import Flask
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.extensions import db, migrate


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models before Flask-Migrate inspects SQLAlchemy metadata.
    from app import models  # noqa: F401
    from app.auth import auth_bp
    from app.line import line_bp
    from app.users import user_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(line_bp, url_prefix="/api/line")
    app.register_blueprint(user_bp, url_prefix="/api")

    @app.get("/api/health")
    def health():
        from app.common.response import api_success

        return api_success({"status": "ok"})

    register_error_handlers(app)
    return app


def register_error_handlers(app):
    from app.common.errors import AppError
    from app.common.response import api_error

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return api_error(
            code=error.code,
            message=error.message,
            status_code=error.status_code,
        )

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return api_error(
            code="VALIDATION_ERROR",
            message="Invalid request data",
            status_code=422,
            details=error.messages,
        )

    @app.errorhandler(HTTPException)
    def handle_http_error(error):
        details = getattr(error, "data", {}).get("messages")
        code = "VALIDATION_ERROR" if error.code == 422 and details else error.name.upper().replace(" ", "_")
        message = "Invalid request data" if code == "VALIDATION_ERROR" else error.description
        return api_error(
            code=code,
            message=message,
            status_code=error.code,
            details=details,
        )
