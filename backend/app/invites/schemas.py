from marshmallow import Schema, fields, validate


class InviteSchema(Schema):
    code = fields.Str(required=True)
    invite_url = fields.Str(required=True)
    nurse_id = fields.Int(allow_none=True)
    created_at = fields.DateTime(required=True)


class InviteProfileCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    language = fields.Str(
        load_default=None,
        allow_none=True,
        validate=validate.Length(max=10),
    )


class InviteEntrySchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(allow_none=True)
    language = fields.Str(allow_none=True)
    role = fields.Str(required=True)
    pair_user_id = fields.Int(allow_none=True)
    needs_profile = fields.Bool(required=True)
