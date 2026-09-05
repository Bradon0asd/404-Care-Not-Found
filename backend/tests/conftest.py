import pytest

from app import create_app
from app.extensions import db


class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LINE_CHANNEL_ACCESS_TOKEN = ""
    LINE_CHANNEL_SECRET = ""
    SECRET_KEY = "test-secret"
    CORS_ORIGINS = ["http://localhost:5173", "https://care.example.com"]


@pytest.fixture()
def app(tmp_path):
    class IsolatedTestConfig(TestConfig):
        UPLOAD_FOLDER = str(tmp_path / "uploads")
        SESSION_FILE_DIR = str(tmp_path / "sessions")

    app = create_app(IsolatedTestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
