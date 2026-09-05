"""Authentication request and response schemas."""

from marshmallow import Schema, fields, validate


class LoginSchema(Schema):
    line_id = fields.Str(required=True, validate=validate.Length(min=1, max=128))


class SessionSchema(Schema):
    id = fields.Int(required=True)
    line_id = fields.Str(required=True)
    name = fields.Str(allow_none=True)
    role = fields.Str(required=True)
    pair_user_id = fields.Int(allow_none=True)
