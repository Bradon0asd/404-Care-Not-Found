from marshmallow import Schema, fields, validate


class UserCreateSchema(Schema):
    line_user_id = fields.Str(required=True, validate=validate.Length(min=1, max=64))
    name = fields.Str(load_default=None, allow_none=True, validate=validate.Length(max=100))


class UserSchema(Schema):
    id = fields.Int(required=True)
    line_user_id = fields.Str(required=True)
    name = fields.Str(allow_none=True)
