import logging

from cachelib.file import FileSystemCache
from flask import Flask
from flask_smorest import Blueprint
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.config import Config
from app.extensions import api, cors, db, migrate, server_session


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)
    configure_api_docs(app)
    configure_uploads(app, config_object)
    configure_session(app, config_object)
    configure_cors(app, config_object)
    configure_logging(app)

    db.init_app(app)
    server_session.init_app(app)
    cors.init_app(
        app,
        resources={
            f"{app.config['UPLOAD_URL_PATH']}/*": {"origins": app.config["CORS_ORIGINS"]},
            r"/api/*": {"origins": app.config["CORS_ORIGINS"]},
        },
        # The session cookie only travels cross-origin when credentials are allowed.
        supports_credentials=True,
        allow_headers=app.config["CORS_ALLOW_HEADERS"],
        methods=app.config["CORS_METHODS"],
        max_age=app.config["CORS_MAX_AGE"],
    )
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
    from app.uploads import media_bp, upload_bp
    from app.users import user_bp
    from app.vital_signs import vital_sign_bp

    api.register_blueprint(auth_bp, url_prefix="/api/auth")
    api.register_blueprint(care_recipient_bp, url_prefix="/api")
    api.register_blueprint(care_schedule_bp, url_prefix="/api")
    api.register_blueprint(diary_bp, url_prefix="/api")
    api.register_blueprint(line_bp, url_prefix="/api/line")
    api.register_blueprint(sticky_note_bp, url_prefix="/api")
    api.register_blueprint(upload_bp, url_prefix="/api")
    api.register_blueprint(user_bp, url_prefix="/api")
    api.register_blueprint(vital_sign_bp, url_prefix="/api")

    health_bp = Blueprint("health", __name__, description="Service health checks")

    @health_bp.get("/health")
    @health_bp.doc(summary="Check API health")
    def health():
        from app.shared.response import api_success

        return api_success({"status": "ok"})

    api.register_blueprint(health_bp, url_prefix="/api")

    app.register_blueprint(media_bp, url_prefix=app.config["UPLOAD_URL_PATH"])

    register_error_handlers(app)
    return app


def configure_logging(app):
    # Hosting platforms only surface stdout/stderr, and the default level hides INFO.
    logging.basicConfig(
        level=logging.WARNING if app.config.get("TESTING") else logging.INFO,
        format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
    )


def configure_cors(app, config_object):
    for key in ("CORS_ORIGINS", "CORS_ALLOW_HEADERS", "CORS_METHODS", "CORS_MAX_AGE"):
        if not hasattr(config_object, key):
            app.config[key] = getattr(Config, key)


def configure_session(app, config_object):
    # Flask ships defaults for SECRET_KEY and the SESSION_COOKIE_* keys, so setdefault would
    # silently keep those instead of ours. Fall back to Config only for keys the caller omitted.
    for key in (
        "SECRET_KEY",
        "SESSION_TYPE",
        "SESSION_FILE_DIR",
        "SESSION_FILE_THRESHOLD",
        "SESSION_PERMANENT",
        "PERMANENT_SESSION_LIFETIME",
        "SESSION_COOKIE_NAME",
        "SESSION_COOKIE_HTTPONLY",
        "SESSION_COOKIE_SAMESITE",
        "SESSION_COOKIE_SECURE",
    ):
        if not hasattr(config_object, key):
            app.config[key] = getattr(Config, key)

    # Built here, not on Config, so a test or deployment can redirect SESSION_FILE_DIR.
    app.config.setdefault(
        "SESSION_CACHELIB",
        FileSystemCache(
            cache_dir=app.config["SESSION_FILE_DIR"],
            threshold=app.config["SESSION_FILE_THRESHOLD"],
        ),
    )


def configure_uploads(app, config_object):
    for key in ("UPLOAD_FOLDER", "UPLOAD_URL_PATH", "MAX_CONTENT_LENGTH", "PUBLIC_BASE_URL"):
        if not hasattr(config_object, key):
            app.config[key] = getattr(Config, key)


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
