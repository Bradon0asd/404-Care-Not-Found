from marshmallow import Schema, fields, validate


class StressSignalCreateSchema(Schema):
    abnormal_count = fields.Int(required=True, validate=validate.Range(min=1))
    occurred_at = fields.DateTime(load_default=None, allow_none=True)


class StressSignalSchema(Schema):
    owner_id = fields.Int(required=True)
    abnormal_count = fields.Int(required=True)
    occurred_at = fields.DateTime(required=True)
