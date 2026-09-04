from marshmallow import Schema, fields, validate

from app.models import ScheduleType


SCHEDULE_TYPES = [schedule_type.value for schedule_type in ScheduleType]


class CareScheduleCreateSchema(Schema):
    schedule_type = fields.Str(required=True, validate=validate.OneOf(SCHEDULE_TYPES))
    weekday = fields.Int(required=True, validate=validate.Range(min=0, max=6))
    start_time = fields.Time(required=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(load_default=None, allow_none=True)


class CareScheduleUpdateSchema(Schema):
    schedule_type = fields.Str(validate=validate.OneOf(SCHEDULE_TYPES))
    weekday = fields.Int(validate=validate.Range(min=0, max=6))
    start_time = fields.Time()
    title = fields.Str(validate=validate.Length(min=1, max=100))
    description = fields.Str(allow_none=True)


class CareScheduleListQuerySchema(Schema):
    schedule_type = fields.Str(validate=validate.OneOf(SCHEDULE_TYPES))


class CareScheduleSchema(Schema):
    id = fields.Int(required=True)
    care_recipient_id = fields.Int(required=True)
    creator_id = fields.Int(required=True)
    schedule_type = fields.Str(required=True)
    weekday = fields.Int(allow_none=True)
    start_time = fields.Time(format="%H:%M", required=True)
    title = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
