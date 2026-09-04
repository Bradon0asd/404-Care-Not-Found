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
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
