from marshmallow import Schema, fields, validate


class DiaryCreateSchema(Schema):
    title = fields.Str(load_default=None, allow_none=True, validate=validate.Length(max=100))
    content = fields.Str(required=True, validate=validate.Length(min=1))


class DiaryUpdateSchema(Schema):
    title = fields.Str(allow_none=True, validate=validate.Length(max=100))
    content = fields.Str(validate=validate.Length(min=1))


class DiarySchema(Schema):
    id = fields.Int(required=True)
    creator_id = fields.Int(required=True)
    title = fields.Str(allow_none=True)
    content = fields.Str(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
