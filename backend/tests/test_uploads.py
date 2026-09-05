import io

PNG_BYTES = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"
    b"\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01"
    b"\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
)


def test_upload_image_returns_a_fetchable_url(client):
    user_id = _create_user(client, "upload-user")

    response = client.post(
        "/api/uploads/image",
        headers=_headers(user_id),
        data={"file": (io.BytesIO(PNG_BYTES), "photo.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 201
    image_url = response.get_json()["data"]["image_url"]
    assert "/uploads/" in image_url
    assert image_url.endswith(".png")

    fetched = client.get(image_url[image_url.index("/uploads/") :])
    assert fetched.status_code == 200
    assert fetched.data == PNG_BYTES


def test_upload_image_requires_authentication(client):
    response = client.post(
        "/api/uploads/image",
        data={"file": (io.BytesIO(PNG_BYTES), "photo.png")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 401


def test_upload_image_rejects_non_image_files(client):
    user_id = _create_user(client, "upload-bad-type")

    response = client.post(
        "/api/uploads/image",
        headers=_headers(user_id),
        data={"file": (io.BytesIO(b"not an image"), "payload.exe")},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "INVALID_UPLOAD"


def test_upload_image_requires_a_file_field(client):
    user_id = _create_user(client, "upload-missing-file")

    response = client.post(
        "/api/uploads/image",
        headers=_headers(user_id),
        data={},
        content_type="multipart/form-data",
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "INVALID_UPLOAD"


def _create_user(client, line_id, *, role="nurse"):
    response = client.post("/api/users", json={"line_id": line_id, "role": role})
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _headers(user_id):
    return {"X-User-Id": str(user_id)}
