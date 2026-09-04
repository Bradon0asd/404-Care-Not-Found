from flask import Flask
from flask_smorest import Blueprint
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.extensions import api, db, migrate


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    configure_api_docs(app)

    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Import models before Flask-Migrate inspects SQLAlchemy metadata.
    from app import models  # noqa: F401
    from app.auth import auth_bp
    from app.care_recipients import care_recipient_bp
    from app.care_schedules import care_schedule_bp
    from app.diaries import diary_bp
    from app.line import line_bp
    from app.sticky_notes import sticky_note_bp
    from app.users import user_bp
    from app.vital_signs import vital_sign_bp

    api.register_blueprint(auth_bp, url_prefix="/api/auth")
    api.register_blueprint(care_recipient_bp, url_prefix="/api")
    api.register_blueprint(care_schedule_bp, url_prefix="/api")
    api.register_blueprint(diary_bp, url_prefix="/api")
    api.register_blueprint(line_bp, url_prefix="/api/line")
    api.register_blueprint(sticky_note_bp, url_prefix="/api")
    api.register_blueprint(user_bp, url_prefix="/api")
    api.register_blueprint(vital_sign_bp, url_prefix="/api")

    health_bp = Blueprint("health", __name__, description="Service health checks")

    @health_bp.get("/health")
    @health_bp.doc(summary="Check API health")
    def health():
        from app.shared.response import api_success

        return api_success({"status": "ok"})

    api.register_blueprint(health_bp, url_prefix="/api")

    register_error_handlers(app)
    return app


def configure_api_docs(app):
    app.config.setdefault("API_TITLE", Config.API_TITLE)
    app.config.setdefault("API_VERSION", Config.API_VERSION)
    app.config.setdefault("OPENAPI_VERSION", Config.OPENAPI_VERSION)
    app.config.setdefault("OPENAPI_URL_PREFIX", Config.OPENAPI_URL_PREFIX)
    app.config.setdefault("OPENAPI_JSON_PATH", Config.OPENAPI_JSON_PATH)
    app.config.setdefault("OPENAPI_SWAGGER_UI_PATH", Config.OPENAPI_SWAGGER_UI_PATH)
    app.config.setdefault("OPENAPI_SWAGGER_UI_URL", Config.OPENAPI_SWAGGER_UI_URL)
    app.config.setdefault("API_SPEC_OPTIONS", Config.API_SPEC_OPTIONS)


def register_error_handlers(app):
    from app.shared.errors import AppError
    from app.shared.response import api_error

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
