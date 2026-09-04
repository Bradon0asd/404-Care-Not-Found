from marshmallow import Schema, ValidationError, fields, validate, validates_schema

from app.models import VitalSignType


VITAL_SIGN_TYPES = [vital_type.value for vital_type in VitalSignType]


class VitalSignCreateSchema(Schema):
    vital_type = fields.Str(required=True, validate=validate.OneOf(VITAL_SIGN_TYPES))
    value = fields.Float(required=True)
    secondary_value = fields.Float(load_default=None, allow_none=True)
    measured_at = fields.DateTime(required=True)
    note = fields.Str(load_default=None, allow_none=True)

    @validates_schema
    def validate_secondary_value(self, data, **kwargs):
        # Blood pressure is the only type carrying two readings (systolic / diastolic).
        is_blood_pressure = data.get("vital_type") == VitalSignType.BLOOD_PRESSURE.value
        secondary_value = data.get("secondary_value")

        if is_blood_pressure and secondary_value is None:
            raise ValidationError(
                "secondary_value is required for blood_pressure",
                field_name="secondary_value",
            )
        if not is_blood_pressure and secondary_value is not None:
            raise ValidationError(
                "secondary_value is only allowed for blood_pressure",
                field_name="secondary_value",
            )


class VitalSignListQuerySchema(Schema):
    vital_type = fields.Str(validate=validate.OneOf(VITAL_SIGN_TYPES))
    start_date = fields.Date()
    end_date = fields.Date()


class VitalSignSchema(Schema):
    id = fields.Int(required=True)
    care_recipient_id = fields.Int(required=True)
    creator_id = fields.Int(required=True)
    vital_type = fields.Str(required=True)
    value = fields.Float(required=True)
    secondary_value = fields.Float(allow_none=True)
    unit = fields.Str(required=True)
    measured_at = fields.DateTime(required=True)
    note = fields.Str(allow_none=True)
    created_at = fields.DateTime(required=True)


class VitalSignMeasurementSchema(Schema):
    value = fields.Float(required=True)
    secondary_value = fields.Float(allow_none=True)
    measured_at = fields.DateTime(required=True)


class VitalSignAverageSchema(Schema):
    value = fields.Float(allow_none=True)
    secondary_value = fields.Float(allow_none=True)


class DashboardMetricSchema(Schema):
    unit = fields.Str(required=True)
    latest = fields.Nested(VitalSignMeasurementSchema, allow_none=True)
    current_average = fields.Nested(VitalSignAverageSchema, allow_none=True)
    previous_average = fields.Nested(VitalSignAverageSchema, allow_none=True)
    difference = fields.Nested(VitalSignAverageSchema, allow_none=True)
    change_text = fields.Str(allow_none=True)


class DashboardPeriodSchema(Schema):
    current_start = fields.DateTime(required=True)
    current_end = fields.DateTime(required=True)
    previous_start = fields.DateTime(required=True)
    previous_end = fields.DateTime(required=True)


class DashboardSchema(Schema):
    period = fields.Nested(DashboardPeriodSchema, required=True)
    blood_pressure = fields.Nested(DashboardMetricSchema, required=True)
    blood_glucose = fields.Nested(DashboardMetricSchema, required=True)
    heart_rate = fields.Nested(DashboardMetricSchema, required=True)
    oxygen_saturation = fields.Nested(DashboardMetricSchema, required=True)
    temperature = fields.Nested(DashboardMetricSchema, required=True)
    respiratory_rate = fields.Nested(DashboardMetricSchema, required=True)
