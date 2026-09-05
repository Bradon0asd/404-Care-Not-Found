from flask import g

from app.auth.decorators import login_required, role_required
from app.auth.service import login, logout
from app.shared.errors import AuthenticationError, PermissionDeniedError


def test_login_creates_a_session_that_survives_requests(client):
    user_id = _create_user(client, "auth-login")

    logged_in = client.post("/api/auth/login", json={"line_id": "auth-login"})
    assert logged_in.status_code == 200
    assert logged_in.get_json()["data"]["id"] == user_id

    # No X-User-Id header; the session cookie alone carries the identity.
    session_read = client.get("/api/auth/session")
    assert session_read.status_code == 200
    assert session_read.get_json()["data"]["line_id"] == "auth-login"


def test_logout_clears_the_session(client):
    _create_user(client, "auth-logout")
    client.post("/api/auth/login", json={"line_id": "auth-logout"})

    logged_out = client.post("/api/auth/logout")
    assert logged_out.status_code == 200

    assert client.get("/api/auth/session").status_code == 401


def test_session_read_requires_login(client):
    response = client.get("/api/auth/session")

    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_login_required_routes_accept_user_id_header(client):
    user_id = _create_user(client, "auth-header")

    response = client.get("/api/users/me", headers=_headers(user_id))

    assert response.status_code == 200
    assert response.get_json()["data"]["line_id"] == "auth-header"


def test_login_rejects_an_unknown_line_id(client):
    response = client.post("/api/auth/login", json={"line_id": "auth-nobody"})

    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_logout_is_safe_without_a_session(client):
    assert client.post("/api/auth/logout").status_code == 200


def test_login_required_decorator_guards_a_view(app, client):
    _create_user(client, "auth-decorated")

    @login_required
    def protected():
        return g.current_user.line_id

    with app.test_request_context():
        try:
            protected()
        except AuthenticationError:
            pass
        else:
            raise AssertionError("login_required should reject an empty session")

        login(line_id="auth-decorated")
        assert protected() == "auth-decorated"

        logout()
        try:
            protected()
        except AuthenticationError:
            pass
        else:
            raise AssertionError("login_required should reject a cleared session")


def test_role_required_decorator_checks_the_session_role(app, client):
    _create_user(client, "auth-nurse-role", role="nurse")

    @role_required("owner")
    def owners_only():
        return "ok"

    with app.test_request_context():
        login(line_id="auth-nurse-role")
        try:
            owners_only()
        except PermissionDeniedError:
            pass
        else:
            raise AssertionError("role_required should reject a nurse")


def _create_user(client, line_id, *, role="nurse"):
    response = client.post("/api/users", json={"line_id": line_id, "role": role})
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _headers(user_id):
    return {"X-User-Id": str(user_id)}
