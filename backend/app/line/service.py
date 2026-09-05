import logging

from app.models import UserRole
from app.users.service import get_or_create_user
from app.line.client import LineClient
from app.line.menu import HELP_REPLY, build_menu_reply


logger = logging.getLogger(__name__)


def handle_text_message(*, line_id, reply_token, text):
    # LINE is the employer channel: whoever talks to the bot is an owner.
    user = get_or_create_user(line_id=line_id, role=UserRole.OWNER.value)
    # Log metadata only. What the caregiver writes stays out of the logs.
    logger.info("line text message received: user_id=%s chars=%s", user.id, len(text))
    reply = build_menu_reply(user=user, text=text) or HELP_REPLY
    LineClient().reply_text(reply_token=reply_token, text=reply)
