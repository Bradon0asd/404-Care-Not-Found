def test_diary_crud_is_limited_to_creator(client):
    creator_id = _create_user(client, "diary-owner")
    other_id = _create_user(client, "diary-other")

    created = client.post(
        "/api/diaries",
        headers=_headers(creator_id),
        json={"title": "Shift notes", "content": "Ate breakfast."},
    )

    assert created.status_code == 201
    diary = created.get_json()["data"]
    assert diary["creator_id"] == creator_id
    assert diary["title"] == "Shift notes"

    denied = client.get(f"/api/diaries/{diary['id']}", headers=_headers(other_id))
    assert denied.status_code == 403

    updated = client.patch(
        f"/api/diaries/{diary['id']}",
        headers=_headers(creator_id),
        json={"content": "Ate breakfast and took medicine."},
    )
    assert updated.status_code == 200
    assert updated.get_json()["data"]["content"] == "Ate breakfast and took medicine."

    deleted = client.delete(f"/api/diaries/{diary['id']}", headers=_headers(creator_id))
    assert deleted.status_code == 200


def test_diary_create_rejects_client_controlled_creator_id(client):
    creator_id = _create_user(client, "diary-controlled")

    response = client.post(
        "/api/diaries",
        headers=_headers(creator_id),
        json={"creator_id": 999, "content": "This should not be accepted."},
    )

    assert response.status_code == 422


def _create_user(client, line_id, *, role="nurse"):
    response = client.post("/api/users", json={"line_id": line_id, "role": role})
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _headers(user_id):
    return {"X-User-Id": str(user_id)}
