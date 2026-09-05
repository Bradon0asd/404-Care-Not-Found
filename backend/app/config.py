import os
import secrets
from datetime import timedelta

from dotenv import load_dotenv
from sqlalchemy.engine import URL


load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parent_env = os.path.join(os.path.dirname(BASE_DIR), ".env")
if os.path.exists(parent_env):
    load_dotenv(parent_env)
backend_env = os.path.join(BASE_DIR, ".env")
if os.path.exists(backend_env):
    load_dotenv(backend_env)


def parse_origins(raw):
    """Split a comma-separated origin list, dropping blanks and trailing slashes."""
    return [origin.strip().rstrip("/") for origin in raw.split(",") if origin.strip()]


def build_database_uri():
    server = os.getenv("DB_SERVER", "127.0.0.1")
    port = 3306
    if ":" in server:
        host, possible_port = server.rsplit(":", 1)
        if possible_port.isdigit():
            server = host
            port = int(possible_port)

    user = os.getenv("DB_USER", "root")
    name = os.getenv("DB_NAME", "hackathon")
    password = os.getenv("DB_PASSWORD", "")
    return URL.create(
        "mysql+pymysql",
        username=user,
        password=password,
        host=server,
        port=port,
        database=name,
        query={"charset": "utf8mb4"},
    ).render_as_string(hide_password=False)


class Config:
    API_TITLE = "Hackathon Backend API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/api/docs"
    OPENAPI_JSON_PATH = "openapi.json"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    API_SPEC_OPTIONS = {
        "components": {
            "securitySchemes": {
                "UserIdHeader": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-User-Id",
                },
                "LineSignature": {
                    "type": "apiKey",
                    "in": "header",
                    "name": "X-Line-Signature",
                },
            }
        }
    }
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEB_APP_BASE_URL = os.getenv("WEB_APP_BASE_URL", "")
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GEMINI_BASE_URL = os.getenv("GEMINI_BASE_URL", "")
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "")
    # Local disk is enough for the demo; set UPLOAD_FOLDER to a mounted volume in production.
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER") or os.path.join(BASE_DIR, "uploads")
    UPLOAD_URL_PATH = "/uploads"
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_UPLOAD_BYTES", 5 * 1024 * 1024))
    # Set when the API is behind a proxy so returned image URLs stay absolute and correct.
    PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "")

    # A generated key keeps dev running without a committed secret, but it changes on every
    # restart and differs per gunicorn worker, so production MUST set SECRET_KEY.
    SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
    # "cachelib" + FileSystemCache is the non-deprecated way to keep sessions on disk.
    SESSION_TYPE = "cachelib"
    SESSION_FILE_DIR = os.getenv("SESSION_FILE_DIR") or os.path.join(BASE_DIR, ".flask_session")
    SESSION_FILE_THRESHOLD = 500
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=int(os.getenv("SESSION_LIFETIME_DAYS", 7)))
    SESSION_COOKIE_NAME = "care_session"
    SESSION_COOKIE_HTTPONLY = True
    # Cross-origin frontends need SameSite=None plus Secure=True; both come from the env.
    SESSION_COOKIE_SAMESITE = os.getenv("SESSION_COOKIE_SAMESITE", "Lax")
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "false").lower() == "true"

    # Credentialed requests forbid a wildcard origin, so the allow list is always explicit.
    # Add the deployed frontend origin through CORS_ORIGINS before going live.
    CORS_ORIGINS = parse_origins(
        os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000",
        )
    )
    # ngrok's free tier serves a warning page unless the request opts out by header,
    # and a header the browser sends must be allowed here or the preflight fails.
    CORS_ALLOW_HEADERS = ["Content-Type", "X-User-Id", "ngrok-skip-browser-warning"]
    CORS_METHODS = ["GET", "POST", "PATCH", "DELETE", "OPTIONS"]
    CORS_MAX_AGE = 600

    # LINE Login (SSO) is a separate channel from the Messaging API bot above.
    LINE_LOGIN_CHANNEL_ID = os.getenv("LINE_LOGIN_CHANNEL_ID", "")
    LINE_LOGIN_CHANNEL_SECRET = os.getenv("LINE_LOGIN_CHANNEL_SECRET", "")
    LINE_LOGIN_CALLBACK_URL = os.getenv("LINE_LOGIN_CALLBACK_URL", "")
    LINE_LOGIN_SCOPE = os.getenv("LINE_LOGIN_SCOPE", "openid profile")
    # "aggressive" or "normal" asks LINE to offer the Official Account during login.
    LINE_LOGIN_BOT_PROMPT = os.getenv("LINE_LOGIN_BOT_PROMPT", "")
    LINE_LOGIN_STATE_TTL = int(os.getenv("LINE_LOGIN_STATE_TTL", 600))
    # Where the callback sends the browser once the session exists (or fails).
    FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
    LINE_LOGIN_SUCCESS_PATH = os.getenv("LINE_LOGIN_SUCCESS_PATH", "/auth/callback")
    LINE_LOGIN_FAILURE_PATH = os.getenv("LINE_LOGIN_FAILURE_PATH", "/auth/role")
