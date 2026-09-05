from sqlalchemy import or_

from app.shared.errors import DiaryNotFoundError, PermissionDeniedError
from app.extensions import db
from app.models import Diary


def create_diary(*, current_user, title=None, content, image_url=None, is_private):
    diary = Diary(
        creator_id=current_user.id,
        title=title,
        content=content,
        image_url=image_url,
        is_private=is_private,
    )
    db.session.add(diary)
    db.session.commit()
    return diary


def list_diaries(*, current_user):
    return (
        Diary.query.filter(_visible_filter(current_user))
        .order_by(Diary.created_at.desc(), Diary.id.desc())
        .all()
    )


def get_diary(*, current_user, diary_id):
    diary = _load_diary(diary_id)
    _require_visible(diary, current_user)
    return diary


def update_diary(*, current_user, diary_id, **changes):
    diary = _load_diary(diary_id)
    _require_creator(diary, current_user)
    for field in ("title", "content", "image_url", "is_private"):
        if field in changes:
            setattr(diary, field, changes[field])
    db.session.commit()
    return diary


def delete_diary(*, current_user, diary_id):
    diary = _load_diary(diary_id)
    _require_creator(diary, current_user)
    db.session.delete(diary)
    db.session.commit()


def _load_diary(diary_id):
    diary = db.session.get(Diary, diary_id)
    if diary is None:
        raise DiaryNotFoundError("Diary not found")
    return diary


def _visible_filter(current_user):
    # Private diaries stay closed; the caregiver alone decides what the paired user sees.
    shared_by_pair = (Diary.creator_id == current_user.pair_user_id) & Diary.is_private.is_(False)
    return or_(Diary.creator_id == current_user.id, shared_by_pair)


def _require_visible(diary, current_user):
    if diary.creator_id == current_user.id:
        return
    if not diary.is_private and diary.creator_id == current_user.pair_user_id:
        return
    raise PermissionDeniedError("Diary is not visible to the current user")


def _require_creator(diary, current_user):
    if diary.creator_id != current_user.id:
        raise PermissionDeniedError("Diary changes are limited to its creator")
