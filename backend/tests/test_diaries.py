def test_diary_crud_is_limited_to_creator(client):
    creator_id = _create_user(client, "diary-owner")
    other_id = _create_user(client, "diary-other")

    created = client.post(
        "/api/diaries",
        headers=_headers(creator_id),
        json={
            "title": "Shift notes",
            "content": "Ate breakfast.",
            "entry_date": "2026-09-05",
            "image_url": "https://example.com/breakfast.png",
        },
    )

    assert created.status_code == 201
    diary = created.get_json()["data"]
    assert diary["creator_id"] == creator_id
    assert diary["title"] == "Shift notes"
    assert diary["entry_date"] == "2026-09-05"
    assert diary["image_url"] == "https://example.com/breakfast.png"
    assert diary["is_private"] is True

    denied = client.get(f"/api/diaries/{diary['id']}", headers=_headers(other_id))
    assert denied.status_code == 403

    updated = client.patch(
        f"/api/diaries/{diary['id']}",
        headers=_headers(creator_id),
        json={"content": "Ate breakfast and took medicine.", "entry_date": "2026-09-06"},
    )
    assert updated.status_code == 200
    assert updated.get_json()["data"]["content"] == "Ate breakfast and took medicine."
    assert updated.get_json()["data"]["entry_date"] == "2026-09-06"

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


def test_diary_visibility_respects_pairing_and_privacy(client):
    nurse_id = _create_user(client, "diary-nurse-pair", role="nurse")
    owner_id = _create_user(client, "diary-owner-pair", role="owner")
    stranger_id = _create_user(client, "diary-stranger", role="owner")
    client.post(f"/api/users/{nurse_id}/pair", json={"pair_user_id": owner_id}, headers=_headers(nurse_id))

    private_id = _create_diary(client, nurse_id, "Kept to myself", is_private=True)
    shared_id = _create_diary(client, nurse_id, "Shared on purpose", is_private=False)

    paired_list = client.get("/api/diaries", headers=_headers(owner_id))
    assert paired_list.status_code == 200
    paired_ids = [item["id"] for item in paired_list.get_json()["data"]]
    assert paired_ids == [shared_id]

    assert client.get(f"/api/diaries/{shared_id}", headers=_headers(owner_id)).status_code == 200
    assert client.get(f"/api/diaries/{private_id}", headers=_headers(owner_id)).status_code == 403
    assert client.get(f"/api/diaries/{shared_id}", headers=_headers(stranger_id)).status_code == 403


def test_shared_diary_cannot_be_changed_by_the_paired_user(client):
    nurse_id = _create_user(client, "diary-nurse-readonly", role="nurse")
    owner_id = _create_user(client, "diary-owner-readonly", role="owner")
    client.post(f"/api/users/{nurse_id}/pair", json={"pair_user_id": owner_id}, headers=_headers(nurse_id))

    shared_id = _create_diary(client, nurse_id, "Shared", is_private=False)

    updated = client.patch(
        f"/api/diaries/{shared_id}",
        headers=_headers(owner_id),
        json={"content": "Edited by the employer."},
    )
    assert updated.status_code == 403

    deleted = client.delete(f"/api/diaries/{shared_id}", headers=_headers(owner_id))
    assert deleted.status_code == 403


def _create_diary(client, user_id, content, *, is_private):
    response = client.post(
        "/api/diaries",
        headers=_headers(user_id),
        json={"content": content, "is_private": is_private},
    )
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _create_user(client, line_id, *, role="nurse"):
    response = client.post("/api/users", json={"line_id": line_id, "role": role})
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _headers(user_id):
    return {"X-User-Id": str(user_id)}
