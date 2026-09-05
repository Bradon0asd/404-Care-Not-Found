from app.config import parse_origins

ALLOWED_ORIGIN = "http://localhost:5173"
SECOND_ALLOWED_ORIGIN = "https://care.example.com"
BLOCKED_ORIGIN = "http://evil.example.com"


def test_preflight_allows_the_configured_origin_with_credentials(client):
    response = client.options(
        "/api/auth/login",
        headers={
            "Origin": ALLOWED_ORIGIN,
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type, X-User-Id",
        },
    )

    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == ALLOWED_ORIGIN
    assert response.headers["Access-Control-Allow-Credentials"] == "true"
    allowed_headers = response.headers["Access-Control-Allow-Headers"]
    assert "X-User-Id" in allowed_headers
    assert "Content-Type" in allowed_headers
    assert "PATCH" in response.headers["Access-Control-Allow-Methods"]


def test_actual_request_carries_cors_headers(client):
    response = client.get("/api/health", headers={"Origin": ALLOWED_ORIGIN})

    assert response.status_code == 200
    assert response.headers["Access-Control-Allow-Origin"] == ALLOWED_ORIGIN
    assert response.headers["Access-Control-Allow-Credentials"] == "true"
    # Caches must not serve one origin's response to another.
    assert "Origin" in response.headers.get("Vary", "")


def test_every_configured_origin_is_allowed(client):
    response = client.get("/api/health", headers={"Origin": SECOND_ALLOWED_ORIGIN})

    assert response.headers["Access-Control-Allow-Origin"] == SECOND_ALLOWED_ORIGIN


def test_unknown_origin_gets_no_cors_grant(client):
    response = client.get("/api/health", headers={"Origin": BLOCKED_ORIGIN})

    assert "Access-Control-Allow-Origin" not in response.headers


def test_uploaded_files_are_reachable_cross_origin(client):
    response = client.get("/uploads/missing.png", headers={"Origin": ALLOWED_ORIGIN})

    assert response.status_code == 404
    assert response.headers["Access-Control-Allow-Origin"] == ALLOWED_ORIGIN


def test_parse_origins_trims_blanks_and_trailing_slashes():
    assert parse_origins(" https://a.example/ , ,https://b.example ") == [
        "https://a.example",
        "https://b.example",
    ]
    assert parse_origins("") == []
