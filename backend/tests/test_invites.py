import pytest

from app.extensions import db
from app.models import Invite, User, UserRole


@pytest.fixture()
def owner_id(app):
    with app.app_context():
        owner = User(line_id="U-employer", role=UserRole.OWNER.value)
        db.session.add(owner)
        db.session.commit()
        return owner.id


def test_owner_creates_an_invite_link(client, owner_id):
    response = client.post("/api/invites", headers=_auth(owner_id))

    assert response.status_code == 201
    data = response.get_json()["data"]
    assert data["code"]
    assert data["invite_url"].endswith(f"/auth/role?invite={data['code']}")
    assert data["nurse_id"] is None


def test_invite_is_reused_instead_of_piling_up(client, owner_id):
    first = client.post("/api/invites", headers=_auth(owner_id)).get_json()["data"]
    second = client.post("/api/invites", headers=_auth(owner_id)).get_json()["data"]

    assert first["code"] == second["code"]


def test_nurse_cannot_create_an_invite(client, app):
    with app.app_context():
        nurse = User(line_id="U-nurse", role=UserRole.NURSE.value)
        db.session.add(nurse)
        db.session.commit()
        nurse_id = nurse.id

    response = client.post("/api/invites", headers=_auth(nurse_id))

    assert response.status_code == 403
    assert response.get_json()["error"]["code"] == "PERMISSION_DENIED"


def test_first_visit_creates_and_pairs_the_caregiver(client, app, owner_id):
    code = _invite_code(client, owner_id)

    response = client.post(f"/api/invites/{code}/enter")

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["role"] == "nurse"
    assert data["needs_profile"] is True
    assert data["pair_user_id"] == owner_id

    with app.app_context():
        owner = db.session.get(User, owner_id)
        assert owner.pair_user_id == data["id"]


def test_returning_visits_land_on_the_same_caregiver(client, owner_id):
    code = _invite_code(client, owner_id)

    first = client.post(f"/api/invites/{code}/enter").get_json()["data"]
    second = client.post(f"/api/invites/{code}/enter").get_json()["data"]

    assert first["id"] == second["id"]


def test_profile_is_saved_on_first_visit(client, owner_id):
    code = _invite_code(client, owner_id)

    response = client.post(
        f"/api/invites/{code}/profile",
        json={"name": "Siti", "language": "id"},
    )

    assert response.status_code == 200
    data = response.get_json()["data"]
    assert data["name"] == "Siti"
    assert data["language"] == "id"
    assert data["needs_profile"] is False


def test_profile_requires_a_name(client, owner_id):
    code = _invite_code(client, owner_id)

    response = client.post(f"/api/invites/{code}/profile", json={})

    assert response.status_code == 422


def test_entering_starts_a_session(client, owner_id):
    code = _invite_code(client, owner_id)
    entered = client.post(f"/api/invites/{code}/enter").get_json()["data"]

    session = client.get("/api/auth/session")

    assert session.status_code == 200
    assert session.get_json()["data"]["id"] == entered["id"]


def test_the_link_signs_the_caregiver_into_the_rest_of_the_api(client, owner_id):
    """After the link, no header is needed: the session cookie carries the identity."""
    code = _invite_code(client, owner_id)
    entered = client.post(f"/api/invites/{code}/enter").get_json()["data"]

    created = client.post("/api/diaries", json={"content": "hari ini baik"})

    assert created.status_code == 201
    assert created.get_json()["data"]["creator_id"] == entered["id"]


def test_requests_without_a_link_or_header_are_rejected(client):
    response = client.get("/api/diaries")

    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_unknown_code_is_rejected(client):
    response = client.post("/api/invites/not-a-real-code/enter")

    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "INVITE_NOT_FOUND"


def test_revoked_code_is_rejected(client, app, owner_id):
    code = _invite_code(client, owner_id)

    with app.app_context():
        invite = Invite.query.filter_by(code=code).first()
        invite.revoked_at = db.func.current_timestamp()
        db.session.commit()

    response = client.post(f"/api/invites/{code}/enter")

    assert response.status_code == 410
    assert response.get_json()["error"]["code"] == "INVITE_REVOKED"


def test_invite_code_is_not_guessable(client, owner_id):
    code = client.post("/api/invites", headers=_auth(owner_id)).get_json()["data"]["code"]

    # The link is the caregiver's only credential, so it must not be short.
    assert len(code) >= 32


def _invite_code(client, owner_id):
    return client.post("/api/invites", headers=_auth(owner_id)).get_json()["data"]["code"]


def _auth(user_id):
    return {"X-User-Id": str(user_id)}
