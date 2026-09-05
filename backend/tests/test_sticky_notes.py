def test_sticky_note_create_list_update_review_delete(client):
    user_id = _create_user(client, "note-owner")

    created = client.post(
        "/api/notes",
        headers=_headers(user_id),
        json={
            "title": "Buy milk",
            "content": "Low lactose, please.",
            "category": "shopping",
            "priority": "normal",
            "images": ["https://example.com/milk.jpg"],
            "is_private": False,
        },
    )

    assert created.status_code == 201
    note = created.get_json()["data"]
    assert note["creator_id"] == user_id
    assert note["images"] == ["https://example.com/milk.jpg"]
    assert note["is_reviewed"] is False

    listed = client.get("/api/notes?category=shopping", headers=_headers(user_id))
    assert listed.status_code == 200
    assert [item["id"] for item in listed.get_json()["data"]] == [note["id"]]

    updated = client.patch(
        f"/api/notes/{note['id']}",
        headers=_headers(user_id),
        json={"priority": "urgent"},
    )
    assert updated.status_code == 200
    assert updated.get_json()["data"]["priority"] == "urgent"

    self_review = client.patch(f"/api/notes/{note['id']}/review", headers=_headers(user_id))
    assert self_review.status_code == 403

    deleted = client.delete(f"/api/notes/{note['id']}", headers=_headers(user_id))
    assert deleted.status_code == 200


def test_sticky_note_visibility_respects_pairing_and_privacy(client):
    owner_id = _create_user(client, "note-owner-pair", role="owner")
    nurse_id = _create_user(client, "note-nurse-pair", role="nurse")
    stranger_id = _create_user(client, "note-stranger", role="nurse")
    client.post(f"/api/users/{owner_id}/pair", json={"pair_user_id": nurse_id}, headers=_headers(owner_id))

    public_note_id = _create_note(client, owner_id, "Public", is_private=False)
    private_note_id = _create_note(client, owner_id, "Private", is_private=True)

    paired_list = client.get("/api/notes", headers=_headers(nurse_id))
    assert paired_list.status_code == 200
    paired_ids = [item["id"] for item in paired_list.get_json()["data"]]
    assert public_note_id in paired_ids
    assert private_note_id not in paired_ids

    stranger_list = client.get("/api/notes", headers=_headers(stranger_id))
    assert stranger_list.status_code == 200
    assert stranger_list.get_json()["data"] == []

    paired_update = client.patch(
        f"/api/notes/{public_note_id}",
        headers=_headers(nurse_id),
        json={"priority": "low"},
    )
    assert paired_update.status_code == 403


def test_public_sticky_note_is_marked_read_by_the_paired_reader(client):
    nurse_id = _create_user(client, "note-nurse-review", role="nurse")
    owner_id = _create_user(client, "note-owner-review", role="owner")
    stranger_id = _create_user(client, "note-stranger-review", role="nurse")
    client.post(f"/api/users/{nurse_id}/pair", json={"pair_user_id": owner_id}, headers=_headers(nurse_id))

    public_note_id = _create_note(client, nurse_id, "Leave request", is_private=False)
    private_note_id = _create_note(client, nurse_id, "Just for me", is_private=True)

    reviewed = client.patch(f"/api/notes/{public_note_id}/review", headers=_headers(owner_id))
    assert reviewed.status_code == 200
    assert reviewed.get_json()["data"]["is_reviewed"] is True

    private_review = client.patch(f"/api/notes/{private_note_id}/review", headers=_headers(owner_id))
    assert private_review.status_code == 403

    stranger_review = client.patch(f"/api/notes/{public_note_id}/review", headers=_headers(stranger_id))
    assert stranger_review.status_code == 403


def test_sticky_note_create_rejects_server_controlled_fields(client):
    user_id = _create_user(client, "note-controlled")

    response = client.post(
        "/api/notes",
        headers=_headers(user_id),
        json={"title": "Oops", "content": "Nope", "creator_id": 5, "is_reviewed": True},
    )

    assert response.status_code == 422


def _create_note(client, user_id, title, *, is_private):
    response = client.post(
        "/api/notes",
        headers=_headers(user_id),
        json={"title": title, "content": title, "is_private": is_private},
    )
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _create_user(client, line_id, *, role="nurse"):
    response = client.post("/api/users", json={"line_id": line_id, "role": role})
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _headers(user_id):
    return {"X-User-Id": str(user_id)}
