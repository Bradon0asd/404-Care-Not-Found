import os
from uuid import uuid4

from flask import current_app, request

from app.shared.errors import InvalidUploadError

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
ALLOWED_MIME_TYPES = {"image/jpeg", "image/png", "image/gif", "image/webp"}


def save_image(file_storage):
    """Store one uploaded image on disk and return its public URL."""
    if file_storage is None or not file_storage.filename:
        raise InvalidUploadError("An image file is required under the 'file' field")

    extension = _extension_of(file_storage.filename)
    if extension not in ALLOWED_EXTENSIONS:
        raise InvalidUploadError(f"Unsupported image type: {sorted(ALLOWED_EXTENSIONS)} only")
    if file_storage.mimetype not in ALLOWED_MIME_TYPES:
        raise InvalidUploadError(f"Unsupported content type: {file_storage.mimetype}")

    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)

    # Generated names keep uploads unguessable and free of client-controlled paths.
    filename = f"{uuid4().hex}.{extension}"
    file_storage.save(os.path.join(folder, filename))
    return build_image_url(filename)


def build_image_url(filename):
    base = current_app.config.get("PUBLIC_BASE_URL") or request.url_root
    url_path = current_app.config["UPLOAD_URL_PATH"].strip("/")
    return f"{base.rstrip('/')}/{url_path}/{filename}"


def _extension_of(filename):
    if "." not in filename:
        return ""
    return filename.rsplit(".", 1)[-1].lower()
