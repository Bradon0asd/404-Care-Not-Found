def test_a_fresh_account_still_needs_onboarding(client):
    _create_user(client, "onboarding-fresh")

    session_read = client.post("/api/auth/login", json={"line_id": "onboarding-fresh"})

    assert session_read.get_json()["data"]["needs_onboarding"] is True


def test_finishing_the_form_saves_the_profile_and_clears_the_flag(client):
    _create_user(client, "onboarding-done")
    client.post("/api/auth/login", json={"line_id": "onboarding-done"})

    completed = client.post(
        "/api/users/me/onboarding",
        json={"name": "Siti", "language": "id"},
    )

    assert completed.status_code == 200
    body = completed.get_json()["data"]
    assert body["name"] == "Siti"
    assert body["language"] == "id"
    assert body["needs_onboarding"] is False

    # The next login is what the frontend routes on, so it has to agree.
    client.post("/api/auth/logout")
    again = client.post("/api/auth/login", json={"line_id": "onboarding-done"})
    assert again.get_json()["data"]["needs_onboarding"] is False


def test_onboarding_requires_a_session(client):
    response = client.post("/api/users/me/onboarding", json={"name": "Nobody"})

    assert response.status_code == 401
    assert response.get_json()["error"]["code"] == "AUTHENTICATION_REQUIRED"


def test_reopening_the_form_keeps_the_original_stamp(app, client):
    from app.models import User

    _create_user(client, "onboarding-twice")
    client.post("/api/auth/login", json={"line_id": "onboarding-twice"})
    client.post("/api/users/me/onboarding", json={"name": "First"})
    first_stamp = User.query.filter_by(line_id="onboarding-twice").one().onboarded_at

    client.post("/api/users/me/onboarding", json={"name": "Second"})
    user = User.query.filter_by(line_id="onboarding-twice").one()

    assert user.name == "Second"
    assert user.onboarded_at == first_stamp


def test_line_signup_lands_before_onboarding(client):
    # A LINE display name arrives with the account, so the name alone cannot say
    # whether this person has been through the setup form.
    created = client.post(
        "/api/users",
        json={"line_id": "onboarding-line", "name": "LINE display name"},
    )

    assert created.get_json()["data"]["needs_onboarding"] is True


def _create_user(client, line_id, *, role="nurse"):
    response = client.post("/api/users", json={"line_id": line_id, "role": role})
    assert response.status_code == 201
    return response.get_json()["data"]["id"]
