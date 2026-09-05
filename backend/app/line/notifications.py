import logging

from app.line.client import LineClient
from app.models import UserRole
from app.shared.errors import LineRecipientNotPairedError, PermissionDeniedError


logger = logging.getLogger(__name__)

STRESS_SIGNAL_TEMPLATE = (
    "照護提醒\n"
    "時間：{occurred_at}\n"
    "需要留意的紀錄：{abnormal_count} 筆\n"
    "建議找個輕鬆的時間關心一下，聊聊最近的工作與生活。"
)


def notify_stress_signal(*, nurse, abnormal_count, occurred_at):
    """Push a stress signal to the nurse's paired owner.

    This function takes no message text on purpose. The owner learns how many
    records need attention and when, never what the nurse wrote.
    """
    owner = _paired_owner(nurse)
    text = STRESS_SIGNAL_TEMPLATE.format(
        occurred_at=occurred_at.strftime("%Y-%m-%d %H:%M"),
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
