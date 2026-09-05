from flask import current_app, request, send_from_directory

from app.auth.current_user import get_current_user
from app.shared.response import api_success
from app.uploads import media_bp, upload_bp
from app.uploads.schemas import ImageUploadSchema
from app.uploads.service import save_image

MULTIPART_IMAGE_BODY = {
    "content": {
        "multipart/form-data": {
            "schema": {
                "type": "object",
                "properties": {"file": {"type": "string", "format": "binary"}},
                "required": ["file"],
            }
        }
    }
}


@upload_bp.post("/uploads/image")
@upload_bp.doc(
    summary="Upload one image and get its URL",
    security=[{"UserIdHeader": []}],
    requestBody=MULTIPART_IMAGE_BODY,
)
def upload_image():
    get_current_user()
    image_url = save_image(request.files.get("file"))
    return api_success(ImageUploadSchema().dump({"image_url": image_url}), status_code=201)


@media_bp.get("/<path:filename>")
def serve_upload(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
