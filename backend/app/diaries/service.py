import logging

from sqlalchemy import or_
from datetime import date

from app.shared.errors import DiaryNotFoundError, PermissionDeniedError
from app.extensions import db
from app.models import Diary, DiaryAiAnalysis, StressSource
from app.stress_signals import service as stress_signals


logger = logging.getLogger(__name__)


def create_diary(*, current_user, title=None, content, entry_date=None, image_url=None, is_private):
    diary = Diary(
        creator_id=current_user.id,
        title=title,
        content=content,
        entry_date=entry_date or date.today(),
        image_url=image_url,
        is_private=is_private,
    )
    db.session.add(diary)
    db.session.commit()
    _detect_stress(diary=diary, current_user=current_user)
    return diary


def list_diaries(*, current_user):
    return (
        Diary.query.filter(_visible_filter(current_user))
        .order_by(Diary.entry_date.desc(), Diary.created_at.desc(), Diary.id.desc())
        .all()
    )


def get_diary(*, current_user, diary_id):
    diary = _load_diary(diary_id)
    _require_visible(diary, current_user)
    return diary


def update_diary(*, current_user, diary_id, **changes):
    diary = _load_diary(diary_id)
    _require_creator(diary, current_user)
    for field in ("title", "content", "entry_date", "image_url", "is_private"):
        if field in changes:
            setattr(diary, field, changes[field])
    db.session.commit()
    return diary


def delete_diary(*, current_user, diary_id):
    diary = _load_diary(diary_id)
    _require_creator(diary, current_user)
    db.session.delete(diary)
    db.session.commit()


def _detect_stress(*, diary, current_user):
    """Read a private diary for strain, and tell the employer a count if it is there.

    Only a diary kept to herself is read. One she chose to share with her employer is
    not her unguarded voice, so it never enters detection — that choice is the point
    of the privacy setting, and reading a shared entry would quietly take it back.

    Whatever happens here, the diary is already saved. Detection failing must never
    cost her the entry she just wrote.
    """
    if not diary.is_private:
        return

    try:
        raised = stress_signals.analyze_and_record(
            nurse=current_user,
            text=diary.content,
            source=StressSource.DIARY.value,
        )
        diary.ai_analysis = (
            DiaryAiAnalysis.EMERGENCY.value if raised else DiaryAiAnalysis.NORMAL.value
        )
        db.session.commit()
    except Exception:
        db.session.rollback()
        logger.exception("diary stress detection failed and was skipped")


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
