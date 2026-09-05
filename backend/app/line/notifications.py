import logging

from app.line.client import LineClient
from app.models import UserRole
from app.shared.errors import LineRecipientNotPairedError, PermissionDeniedError


logger = logging.getLogger(__name__)

STRESS_SIGNAL_TEMPLATE = "\n".join(
    [
        "【{date}】【壓力告知】通知內容",
        "本日看護壓力偵測異常筆數：{abnormal_count} 筆",
        "時間點：{occurred_time}",
        "建議關心一下看護今日心理狀況",
        "友善職場 從你我的關心開始！",
    ]
)


def notify_stress_signal(*, nurse, abnormal_count, occurred_at):
    """Push a stress signal to the nurse's paired owner.

    This function takes no message text on purpose. The owner learns how many
    records need attention and when, never what the nurse wrote.
    """
    owner = _paired_owner(nurse)
    text = STRESS_SIGNAL_TEMPLATE.format(
        date=occurred_at.strftime("%m%d"),
        occurred_time=occurred_at.strftime("%H:%M"),
        abnormal_count=abnormal_count,
    )
    LineClient().push_text(user_id=owner.line_id, text=text)
    logger.info(
        "stress signal delivered: nurse_id=%s owner_id=%s count=%s",
        nurse.id,
        owner.id,
        abnormal_count,
    )
    return owner


def _paired_owner(nurse):
    if nurse.role != UserRole.NURSE.value:
        raise PermissionDeniedError("Stress signals can only be raised by a nurse")

    owner = nurse.paired_user
    if owner is None or owner.role != UserRole.OWNER.value:
        raise LineRecipientNotPairedError("Nurse is not paired with an owner")

    return owner
