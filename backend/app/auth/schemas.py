"""Authentication request and response schemas."""

from marshmallow import Schema, fields, validate

from app.models import UserRole


class LoginSchema(Schema):
    line_id = fields.Str(required=True, validate=validate.Length(min=1, max=128))


class SessionSchema(Schema):
    id = fields.Int(required=True)
    line_id = fields.Str(required=True)
    name = fields.Str(allow_none=True)
    picture_url = fields.Url(allow_none=True)
    role = fields.Str(required=True)
    pair_user_id = fields.Int(allow_none=True)
    # The frontend routes on this instead of guessing from the profile fields.
    needs_onboarding = fields.Bool(required=True)


class LineLoginStartSchema(Schema):
    role = fields.Str(required=True, validate=validate.OneOf([role.value for role in UserRole]))


class LineLoginStartResponseSchema(Schema):
    authorization_url = fields.Str(required=True)
