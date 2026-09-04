def test_create_and_get_user(client):
    created = client.post(
        "/api/users",
        json={"line_id": "U123", "name": "Ada"},
    )
    assert created.status_code == 201

    response = client.get(f"/api/users/{created.get_json()['id']}")
    assert response.status_code == 200
    assert response.get_json()["line_id"] == "U123"


def test_create_user_validates_json(client):
    response = client.post("/api/users", json={})

    assert response.status_code == 422
