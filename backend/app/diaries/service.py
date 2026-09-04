from app.shared.errors import DiaryNotFoundError, PermissionDeniedError
from app.extensions import db
from app.models import Diary


def create_diary(*, current_user, title=None, content):
    diary = Diary(creator_id=current_user.id, title=title, content=content)
    db.session.add(diary)
    db.session.commit()
    return diary


def list_diaries(*, current_user):
    return (
        Diary.query.filter_by(creator_id=current_user.id)
        .order_by(Diary.created_at.desc(), Diary.id.desc())
        .all()
    )


def get_diary(*, current_user, diary_id):
    diary = db.session.get(Diary, diary_id)
    if diary is None:
        raise DiaryNotFoundError("Diary not found")
    _require_creator(diary, current_user)
    return diary


def update_diary(*, current_user, diary_id, **changes):
    diary = get_diary(current_user=current_user, diary_id=diary_id)
    for field in ("title", "content"):
        if field in changes:
            setattr(diary, field, changes[field])
    db.session.commit()
    return diary


def delete_diary(*, current_user, diary_id):
    diary = get_diary(current_user=current_user, diary_id=diary_id)
    db.session.delete(diary)
    db.session.commit()


def _require_creator(diary, current_user):
    if diary.creator_id != current_user.id:
        raise PermissionDeniedError("Diary access is limited to its creator")
