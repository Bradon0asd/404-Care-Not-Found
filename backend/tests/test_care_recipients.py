def test_owner_creates_recipient_and_paired_nurse_sees_it(client):
    owner_id = _create_user(client, "recipient-owner", role="owner")
    nurse_id = _create_user(client, "recipient-nurse", role="nurse")
    paired = client.post(f"/api/users/{owner_id}/pair", json={"pair_user_id": nurse_id}, headers=_headers(owner_id))
    assert paired.status_code == 200

    created = client.post(
        "/api/care-recipients",
        headers=_headers(owner_id),
        json={"name": "阿嬤"},
    )
    assert created.status_code == 201
    recipient = created.get_json()["data"]
    assert recipient["name"] == "阿嬤"
    assert recipient["owner_id"] == owner_id
    assert recipient["nurse_id"] == nurse_id

    nurse_list = client.get("/api/care-recipients", headers=_headers(nurse_id))
    assert nurse_list.status_code == 200
    assert [item["id"] for item in nurse_list.get_json()["data"]] == [recipient["id"]]

    fetched = client.get(f"/api/care-recipients/{recipient['id']}", headers=_headers(nurse_id))
    assert fetched.status_code == 200
    assert fetched.get_json()["data"]["name"] == "阿嬤"

    renamed = client.patch(
        f"/api/care-recipients/{recipient['id']}",
        headers=_headers(nurse_id),
        json={"name": "阿公"},
    )
    assert renamed.status_code == 200
    assert renamed.get_json()["data"]["name"] == "阿公"


def test_nurse_creates_recipient_for_its_paired_owner(client):
    owner_id = _create_user(client, "nurse-side-owner", role="owner")
    nurse_id = _create_user(client, "nurse-side-nurse", role="nurse")
    client.post(f"/api/users/{owner_id}/pair", json={"pair_user_id": nurse_id}, headers=_headers(owner_id))

    created = client.post(
        "/api/care-recipients",
        headers=_headers(nurse_id),
        json={"name": "阿嬤"},
    )
    assert created.status_code == 201
    recipient = created.get_json()["data"]
    assert recipient["owner_id"] == owner_id
    assert recipient["nurse_id"] == nurse_id


def test_unpaired_owner_creates_recipient_without_nurse(client):
    owner_id = _create_user(client, "solo-owner", role="owner")

    created = client.post(
        "/api/care-recipients",
        headers=_headers(owner_id),
        json={"name": "阿嬤"},
    )
    assert created.status_code == 201
    assert created.get_json()["data"]["nurse_id"] is None


def test_unpaired_nurse_cannot_create_recipient(client):
    nurse_id = _create_user(client, "solo-nurse", role="nurse")

    response = client.post(
        "/api/care-recipients",
        headers=_headers(nurse_id),
        json={"name": "阿嬤"},
    )
    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "CARE_RECIPIENT_OWNER_REQUIRED"


def test_recipient_is_hidden_from_unrelated_users(client):
    owner_id = _create_user(client, "hidden-owner", role="owner")
    stranger_id = _create_user(client, "hidden-stranger", role="nurse")
    created = client.post(
        "/api/care-recipients",
        headers=_headers(owner_id),
        json={"name": "阿嬤"},
    )
    recipient_id = created.get_json()["data"]["id"]

    listed = client.get("/api/care-recipients", headers=_headers(stranger_id))
    assert listed.status_code == 200
    assert listed.get_json()["data"] == []

    fetched = client.get(f"/api/care-recipients/{recipient_id}", headers=_headers(stranger_id))
    assert fetched.status_code == 403
    assert fetched.get_json()["error"]["code"] == "PERMISSION_DENIED"

    missing = client.get("/api/care-recipients/9999", headers=_headers(owner_id))
    assert missing.status_code == 404
    assert missing.get_json()["error"]["code"] == "CARE_RECIPIENT_NOT_FOUND"


def test_recipient_create_rejects_server_controlled_fields(client):
    owner_id = _create_user(client, "controlled-owner", role="owner")

    response = client.post(
        "/api/care-recipients",
        headers=_headers(owner_id),
        json={"name": "阿嬤", "owner_id": 999, "nurse_id": 999},
    )
    assert response.status_code == 422


def test_recipient_endpoints_support_the_schedule_and_dashboard_flow(client):
    owner_id = _create_user(client, "flow-owner", role="owner")
    nurse_id = _create_user(client, "flow-nurse", role="nurse")
    client.post(f"/api/users/{owner_id}/pair", json={"pair_user_id": nurse_id}, headers=_headers(owner_id))

    created = client.post(
        "/api/care-recipients",
        headers=_headers(nurse_id),
        json={"name": "阿嬤"},
    )
    recipient_id = created.get_json()["data"]["id"]

    schedule = client.post(
        f"/api/care-recipients/{recipient_id}/schedules",
        headers=_headers(nurse_id),
        json={
            "schedule_type": "weekday",
            "weekday": 0,
            "start_time": "09:00",
            "title": "吃胃藥",
        },
    )
    assert schedule.status_code == 201

    vital_sign = client.post(
        f"/api/care-recipients/{recipient_id}/vital-signs",
        headers=_headers(nurse_id),
        json={
            "vital_type": "blood_glucose",
            "value": 80,
            "measured_at": "2026-09-05T09:30:00",
        },
    )
    assert vital_sign.status_code == 201

    dashboard = client.get(
        f"/api/care-recipients/{recipient_id}/dashboard",
        headers=_headers(nurse_id),
    )
    assert dashboard.status_code == 200
    assert dashboard.get_json()["data"]["blood_glucose"]["unit"] == "mg/dL"


def _create_user(client, line_id, *, role="nurse"):
    response = client.post("/api/users", json={"line_id": line_id, "role": role})
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _headers(user_id):
    return {"X-User-Id": str(user_id)}
