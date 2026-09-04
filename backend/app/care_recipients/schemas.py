from marshmallow import Schema, fields, validate


class CareRecipientCreateSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))


class CareRecipientUpdateSchema(Schema):
    name = fields.Str(validate=validate.Length(min=1, max=100))


class CareRecipientSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    owner_id = fields.Int(required=True)
    nurse_id = fields.Int(allow_none=True)
    created_at = fields.DateTime(required=True)
