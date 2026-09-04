from marshmallow import Schema, fields, validate

from app.models import StickyNoteCategory, StickyNotePriority


class StickyNoteCreateSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(
        load_default=None,
        allow_none=True,
        validate=validate.OneOf([category.value for category in StickyNoteCategory]),
    )
    priority = fields.Str(
        load_default=StickyNotePriority.NORMAL.value,
        validate=validate.OneOf([priority.value for priority in StickyNotePriority]),
    )
    images = fields.List(fields.Str(), load_default=list)
    is_private = fields.Bool(load_default=False)


class StickyNoteUpdateSchema(Schema):
    title = fields.Str(validate=validate.Length(min=1, max=100))
    content = fields.Str(validate=validate.Length(min=1))
    category = fields.Str(
        allow_none=True,
        validate=validate.OneOf([category.value for category in StickyNoteCategory]),
    )
    priority = fields.Str(
        validate=validate.OneOf([priority.value for priority in StickyNotePriority]),
    )
    images = fields.List(fields.Str())
    is_private = fields.Bool()


class StickyNoteListQuerySchema(Schema):
    category = fields.Str(
        validate=validate.OneOf([category.value for category in StickyNoteCategory]),
    )
    priority = fields.Str(
        validate=validate.OneOf([priority.value for priority in StickyNotePriority]),
    )
    is_reviewed = fields.Bool()


class StickyNoteSchema(Schema):
    id = fields.Int(required=True)
    creator_id = fields.Int(required=True)
    title = fields.Str(required=True)
    content = fields.Str(required=True)
    category = fields.Str(allow_none=True)
    priority = fields.Str(required=True)
    images = fields.List(fields.Str(), required=True)
    is_reviewed = fields.Bool(required=True)
    is_private = fields.Bool(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
