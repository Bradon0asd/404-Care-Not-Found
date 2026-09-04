from app.auth.current_user import get_current_user
from app.shared.response import api_success
from app.sticky_notes import service as sticky_note_service
from app.sticky_notes import sticky_note_bp
from app.sticky_notes.schemas import (
    StickyNoteCreateSchema,
    StickyNoteListQuerySchema,
    StickyNoteSchema,
    StickyNoteUpdateSchema,
)


@sticky_note_bp.post("/notes")
@sticky_note_bp.arguments(StickyNoteCreateSchema, location="json")
@sticky_note_bp.doc(summary="Create a sticky note", security=[{"UserIdHeader": []}])
def create_note(args):
    note = sticky_note_service.create_note(current_user=get_current_user(), **args)
    return api_success(StickyNoteSchema().dump(note), status_code=201)


@sticky_note_bp.get("/notes")
@sticky_note_bp.arguments(StickyNoteListQuerySchema, location="query")
@sticky_note_bp.doc(summary="List sticky notes", security=[{"UserIdHeader": []}])
def list_notes(args):
    notes = sticky_note_service.list_notes(current_user=get_current_user(), **args)
    return api_success(StickyNoteSchema(many=True).dump(notes))


@sticky_note_bp.get("/notes/<int:note_id>")
@sticky_note_bp.doc(summary="Get a sticky note", security=[{"UserIdHeader": []}])
def get_note(note_id):
    note = sticky_note_service.get_note(current_user=get_current_user(), note_id=note_id)
    return api_success(StickyNoteSchema().dump(note))


@sticky_note_bp.patch("/notes/<int:note_id>")
@sticky_note_bp.arguments(StickyNoteUpdateSchema, location="json")
@sticky_note_bp.doc(summary="Update a sticky note", security=[{"UserIdHeader": []}])
def update_note(args, note_id):
    note = sticky_note_service.update_note(
        current_user=get_current_user(),
        note_id=note_id,
        **args,
    )
    return api_success(StickyNoteSchema().dump(note))


@sticky_note_bp.patch("/notes/<int:note_id>/review")
@sticky_note_bp.doc(summary="Mark a sticky note as reviewed", security=[{"UserIdHeader": []}])
def review_note(note_id):
    note = sticky_note_service.review_note(current_user=get_current_user(), note_id=note_id)
    return api_success(StickyNoteSchema().dump(note))


@sticky_note_bp.delete("/notes/<int:note_id>")
@sticky_note_bp.doc(summary="Delete a sticky note", security=[{"UserIdHeader": []}])
def delete_note(note_id):
    sticky_note_service.delete_note(current_user=get_current_user(), note_id=note_id)
    return api_success()
