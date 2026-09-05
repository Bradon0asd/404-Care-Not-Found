from sqlalchemy import or_

from app.shared.errors import PermissionDeniedError, StickyNoteNotFoundError
from app.extensions import db
from app.models import StickyNote


def create_note(
    *,
    current_user,
    title,
    content,
    category=None,
    priority="normal",
    images=None,
    is_private=False,
):
    note = StickyNote(
        creator_id=current_user.id,
        title=title,
        content=content,
        category=category,
        priority=priority,
        images=images or [],
        is_private=is_private,
        is_reviewed=False,
    )
    db.session.add(note)
    db.session.commit()
    return note


def list_notes(*, current_user, category=None, priority=None, is_reviewed=None):
    query = StickyNote.query.filter(_visible_filter(current_user))

    if category is not None:
        query = query.filter(StickyNote.category == category)
    if priority is not None:
        query = query.filter(StickyNote.priority == priority)
    if is_reviewed is not None:
        query = query.filter(StickyNote.is_reviewed.is_(is_reviewed))

    return query.order_by(StickyNote.created_at.desc(), StickyNote.id.desc()).all()


def get_note(*, current_user, note_id):
    note = db.session.get(StickyNote, note_id)
    if note is None:
        raise StickyNoteNotFoundError("Sticky note not found")
    _require_visible(note, current_user)
    return note


def update_note(*, current_user, note_id, **changes):
    note = db.session.get(StickyNote, note_id)
    if note is None:
        raise StickyNoteNotFoundError("Sticky note not found")
    _require_creator(note, current_user)

    for field in ("title", "content", "category", "priority", "images", "is_private"):
        if field in changes:
            setattr(note, field, changes[field])
    db.session.commit()
    return note


def review_note(*, current_user, note_id):
    """Mark a note as read. Only the paired reader does this, never the author."""
    note = db.session.get(StickyNote, note_id)
    if note is None:
        raise StickyNoteNotFoundError("Sticky note not found")
    _require_visible(note, current_user)
    if note.creator_id == current_user.id:
        raise PermissionDeniedError("Sticky note review is limited to its reader")

    note.is_reviewed = True
    db.session.commit()
    return note


def delete_note(*, current_user, note_id):
    note = db.session.get(StickyNote, note_id)
    if note is None:
        raise StickyNoteNotFoundError("Sticky note not found")
    _require_creator(note, current_user)

    db.session.delete(note)
    db.session.commit()


def _visible_filter(current_user):
    public_pair_filter = StickyNote.creator_id == current_user.pair_user_id
    return or_(StickyNote.creator_id == current_user.id, public_pair_filter & StickyNote.is_private.is_(False))


def _require_visible(note, current_user):
    if note.creator_id == current_user.id:
        return
    if not note.is_private and note.creator_id == current_user.pair_user_id:
        return
    raise PermissionDeniedError("Sticky note is not visible to the current user")


def _require_creator(note, current_user):
    if note.creator_id != current_user.id:
        raise PermissionDeniedError("Sticky note changes are limited to its creator")
