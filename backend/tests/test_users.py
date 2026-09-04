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
