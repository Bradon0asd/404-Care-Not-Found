import logging

from app.users.service import get_or_create_user
from app.line.client import LineClient


logger = logging.getLogger(__name__)


def handle_text_message(*, line_id, reply_token, text):
    user = get_or_create_user(line_id=line_id)
    # Log metadata only. What the caregiver writes stays out of the logs.
    logger.info("line text message received: user_id=%s chars=%s", user.id, len(text))
    reply = f"收到：{text}"
    LineClient().reply_text(reply_token=reply_token, text=reply)
