def test_openapi_docs_include_registered_routes(client):
    response = client.get("/api/docs/openapi.json")

    assert response.status_code == 200

    spec = response.get_json()
    assert spec["info"]["title"] == "Hackathon Backend API"
    assert "/api/health" in spec["paths"]
    assert "/api/users" in spec["paths"]
    assert "/api/diaries" in spec["paths"]
    assert "/api/notes" in spec["paths"]


def test_swagger_ui_is_available(client):
    response = client.get("/api/docs/swagger")

    assert response.status_code == 200
