from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    line_id = fields.Str(required=True, validate=validate.Length(min=1, max=128))
    name = fields.Str(load_default=None, allow_none=True, validate=validate.Length(max=100))
    language = fields.Str(
        load_default=None,
        allow_none=True,
        validate=validate.Length(max=10),
    )
    role = fields.Str(
        load_default="nurse",
        validate=validate.OneOf(["owner", "nurse"]),
    )


class UserSchema(Schema):
    id = fields.Int(required=True)
    line_id = fields.Str(required=True)
    name = fields.Str(allow_none=True)
    language = fields.Str(allow_none=True)
    role = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
