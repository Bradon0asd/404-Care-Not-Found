from app.users.service import get_or_create_user
from app.line.client import LineClient


def handle_text_message(*, line_id, reply_token, text):
    get_or_create_user(line_id=line_id)
    reply = f"收到：{text}"
    LineClient().reply_text(reply_token=reply_token, text=reply)
