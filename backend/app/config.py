import os

from dotenv import load_dotenv
from sqlalchemy.engine import URL


load_dotenv()


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
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
