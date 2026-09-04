from flask import Flask
from marshmallow import ValidationError

from app.config import Config
from app.extensions import db, migrate


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import models before Flask-Migrate inspects SQLAlchemy metadata.
    from app import models  # noqa: F401
    from app.api import api_bp
    from app.auth import auth_bp
    from app.line import line_bp

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(line_bp, url_prefix="/api/line")

    register_error_handlers(app)
    return app


def register_error_handlers(app):
    from app.common.errors import AppError

    @app.errorhandler(AppError)
    def handle_app_error(error):
        return {
            "error": {"code": error.code, "message": error.message}
        }, error.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        return {
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid request data",
                "details": error.messages,
            }
        }, 422
