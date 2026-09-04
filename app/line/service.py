from app.api.service import get_or_create_user
from app.line.client import LineClient


def handle_text_message(*, line_user_id, reply_token, text):
    get_or_create_user(line_user_id=line_user_id)
    reply = f"收到：{text}"
    LineClient().reply_text(reply_token=reply_token, text=reply)
