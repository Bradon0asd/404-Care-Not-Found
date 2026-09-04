def test_create_and_get_user(client):
    created = client.post(
        "/api/users",
        json={"line_id": "U123", "name": "Ada"},
    )
    assert created.status_code == 201

    created_body = created.get_json()
    assert created_body["success"] is True

    response = client.get(f"/api/users/{created_body['data']['id']}")
    assert response.status_code == 200
    body = response.get_json()
    assert body["success"] is True
    assert body["data"]["line_id"] == "U123"


def test_create_user_validates_json(client):
    response = client.post("/api/users", json={})

    assert response.status_code == 422
    body = response.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "VALIDATION_ERROR"


def test_owner_pairs_with_nurse(client):
    owner_id = _create_user(client, "owner-1", role="owner")
    nurse_id = _create_user(client, "nurse-1", role="nurse")

    response = client.post(
        f"/api/users/{owner_id}/pair",
        json={"pair_user_id": nurse_id},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["success"] is True
    assert body["data"]["id"] == owner_id
    assert body["data"]["pair_user_id"] == nurse_id

    nurse = client.get(f"/api/users/{nurse_id}").get_json()
    assert nurse["data"]["pair_user_id"] == owner_id


def test_nurse_pairs_with_owner(client):
    owner_id = _create_user(client, "owner-2", role="owner")
    nurse_id = _create_user(client, "nurse-2", role="nurse")

    response = client.post(
        f"/api/users/{nurse_id}/pair",
        json={"pair_user_id": owner_id},
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["data"]["id"] == nurse_id
    assert body["data"]["pair_user_id"] == owner_id

    owner = client.get(f"/api/users/{owner_id}").get_json()
    assert owner["data"]["pair_user_id"] == nurse_id


def test_pair_user_rejects_self_pairing(client):
    owner_id = _create_user(client, "owner-self", role="owner")

    response = client.post(
        f"/api/users/{owner_id}/pair",
        json={"pair_user_id": owner_id},
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "USER_PAIRING_ERROR"


def test_pair_user_rejects_same_role_pairing(client):
    first_owner_id = _create_user(client, "owner-same-1", role="owner")
    second_owner_id = _create_user(client, "owner-same-2", role="owner")

    response = client.post(
        f"/api/users/{first_owner_id}/pair",
        json={"pair_user_id": second_owner_id},
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "USER_PAIRING_ERROR"


def test_pair_user_rejects_already_paired_users(client):
    owner_id = _create_user(client, "owner-paired", role="owner")
    first_nurse_id = _create_user(client, "nurse-paired-1", role="nurse")
    second_nurse_id = _create_user(client, "nurse-paired-2", role="nurse")
    client.post(f"/api/users/{owner_id}/pair", json={"pair_user_id": first_nurse_id})

    response = client.post(
        f"/api/users/{owner_id}/pair",
        json={"pair_user_id": second_nurse_id},
    )

    assert response.status_code == 400
    body = response.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "USER_PAIRING_ERROR"


def test_unpair_user_clears_both_sides(client):
    owner_id = _create_user(client, "owner-unpair", role="owner")
    nurse_id = _create_user(client, "nurse-unpair", role="nurse")
    client.post(f"/api/users/{owner_id}/pair", json={"pair_user_id": nurse_id})

    response = client.delete(f"/api/users/{owner_id}/pair")

    assert response.status_code == 200
    body = response.get_json()
    assert body["data"]["pair_user_id"] is None

    nurse = client.get(f"/api/users/{nurse_id}").get_json()
    assert nurse["data"]["pair_user_id"] is None


def _create_user(client, line_id, *, role):
    response = client.post(
        "/api/users",
        json={"line_id": line_id, "role": role},
    )
    assert response.status_code == 201
    return response.get_json()["data"]["id"]
