import os
from urllib.parse import quote_plus

from dotenv import load_dotenv


load_dotenv()


def build_database_uri():
    server = os.getenv("DB_SERVER", "127.0.0.1:3306")
    name = os.getenv("DB_NAME", "hackathon")
    password = quote_plus(os.getenv("DB_PASSWORD", ""))
    return f"mysql+pymysql://root:{password}@{server}/{name}?charset=utf8mb4"


class Config:
    SQLALCHEMY_DATABASE_URI = build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "")
    LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "")
