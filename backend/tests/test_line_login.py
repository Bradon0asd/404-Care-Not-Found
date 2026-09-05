from urllib.parse import parse_qs, urlparse

import pytest

from app.auth import service as auth_service
from app.auth.line_client import LineLoginClient
from app.models import User


@pytest.fixture()
def login_app(app):
    app.config.update(
        LINE_LOGIN_CHANNEL_ID="login-channel-id",
        LINE_LOGIN_CHANNEL_SECRET="login-channel-secret",
        LINE_LOGIN_CALLBACK_URL="http://localhost:5000/api/auth/line/callback",
        FRONTEND_URL="http://localhost:5173",
    )
    return app


@pytest.fixture()
def line_identity(monkeypatch):
    """Stub the LINE round trip; the test decides which LINE account comes back."""
    identity = {"user_id": "U-line-login", "display_name": "Mia"}

    def fetch_identity(self, *, code):
        assert code
        return identity["user_id"], identity["display_name"]

    monkeypatch.setattr(LineLoginClient, "fetch_identity", fetch_identity)
    return identity


def test_start_returns_a_line_authorization_url(login_app, client):
    response = client.post("/api/auth/line/start", json={"role": "nurse"})

    assert response.status_code == 200
    url = response.get_json()["data"]["authorization_url"]
    query = parse_qs(urlparse(url).query)
    assert url.startswith("https://access.line.me/oauth2/v2.1/authorize")
    assert query["client_id"] == ["login-channel-id"]
    assert query["response_type"] == ["code"]
    assert query["scope"] == ["openid profile"]
    assert query["state"][0]


def test_start_rejects_an_unknown_role(login_app, client):
    response = client.post("/api/auth/line/start", json={"role": "caregiver"})

    assert response.status_code == 422
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_start_without_configuration_reports_it(app, client):
    response = client.post("/api/auth/line/start", json={"role": "nurse"})

    assert response.status_code == 503
    assert response.get_json()["error"]["code"] == "LINE_LOGIN_NOT_CONFIGURED"


def test_first_login_creates_the_user_with_the_selected_role(login_app, client, line_identity):
    response = _login(client, "owner")

    assert response.status_code == 302
    location = urlparse(response.headers["Location"])
    assert location.path == "/auth/callback"
    assert parse_qs(location.query)["role"] == ["owner"]

    user = User.query.filter_by(line_id="U-line-login").one()
    assert user.role == "owner"
    assert user.name == "Mia"

    me = client.get("/api/users/me")
    assert me.status_code == 200
    body = me.get_json()["data"]
    assert (body["id"], body["name"], body["role"]) == (user.id, "Mia", "owner")


def test_second_login_reuses_the_user_and_keeps_the_stored_role(login_app, client, line_identity):
    _login(client, "nurse")
    user_id = User.query.filter_by(line_id="U-line-login").one().id

    line_identity["display_name"] = "Renamed"
    assert _login(client, "nurse").status_code == 302

    users = User.query.filter_by(line_id="U-line-login").all()
    assert [user.id for user in users] == [user_id]
    assert users[0].role == "nurse"


def test_login_cannot_rewrite_an_existing_role(login_app, client, line_identity):
    _login(client, "nurse")

    response = _login(client, "owner")

    assert response.status_code == 302
    assert parse_qs(urlparse(response.headers["Location"]).query)["error"] == ["ROLE_MISMATCH"]
    assert User.query.filter_by(line_id="U-line-login").one().role == "nurse"


def test_state_cannot_be_replayed(login_app, client, line_identity):
    state = _start(client, "nurse")
    client.get(f"/api/auth/line/callback?code=line-code&state={state}")

    response = client.get(f"/api/auth/line/callback?code=line-code&state={state}")

    assert parse_qs(urlparse(response.headers["Location"]).query)["error"] == ["LINE_LOGIN_FAILED"]


def test_callback_rejects_an_unknown_state(login_app, client, line_identity):
    response = client.get("/api/auth/line/callback?code=line-code&state=forged")

    assert parse_qs(urlparse(response.headers["Location"]).query)["error"] == ["LINE_LOGIN_FAILED"]
    assert User.query.count() == 0


def test_callback_without_a_code_fails(login_app, client, line_identity):
    state = _start(client, "nurse")

    response = client.get(f"/api/auth/line/callback?state={state}")

    assert parse_qs(urlparse(response.headers["Location"]).query)["error"] == ["LINE_LOGIN_FAILED"]


def test_state_expires(login_app, client, line_identity):
    login_app.config["LINE_LOGIN_STATE_TTL"] = -1
    state = _start(client, "nurse")

    response = client.get(f"/api/auth/line/callback?code=line-code&state={state}")

    assert parse_qs(urlparse(response.headers["Location"]).query)["error"] == ["LINE_LOGIN_FAILED"]


def test_current_user_requires_a_session(login_app, client):
    response = client.get("/api/users/me")

    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_line_login_shares_the_existing_session(login_app, client, line_identity):
    _login(client, "nurse")

    session_read = client.get("/api/auth/session")
    assert session_read.status_code == 200
    assert session_read.get_json()["data"]["line_id"] == "U-line-login"

    client.post("/api/auth/logout")
    assert client.get("/api/users/me").status_code == 401


def test_state_store_holds_the_role(login_app):
    with login_app.test_request_context():
        url = auth_service.start_line_login(role="owner")
        state = parse_qs(urlparse(url).query)["state"][0]
        assert auth_service.consume_login_state(state) == "owner"


def _start(client, role):
    response = client.post("/api/auth/line/start", json={"role": role})
    assert response.status_code == 200
    url = response.get_json()["data"]["authorization_url"]
    return parse_qs(urlparse(url).query)["state"][0]


def _login(client, role):
    state = _start(client, role)
    return client.get(f"/api/auth/line/callback?code=line-code&state={state}")
