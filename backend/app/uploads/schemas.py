from marshmallow import Schema, fields


class ImageUploadSchema(Schema):
    image_url = fields.Str(required=True)
