from flask import current_app, request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from app.shared.errors import InvalidLineSignatureError, LineConfigurationError
from app.shared.response import api_success
from app.line import line_bp
from app.line.service import handle_text_message


@line_bp.post("/webhook")
@line_bp.doc(summary="Receive LINE webhook events", security=[{"LineSignature": []}])
def webhook():
    secret = current_app.config["LINE_CHANNEL_SECRET"]
    if not secret:
        raise LineConfigurationError("LINE channel secret is not configured")

    body = request.get_data(as_text=True)
    signature = request.headers.get("X-Line-Signature", "")
    try:
        events = WebhookParser(secret).parse(body, signature)
    except InvalidSignatureError as error:
        raise InvalidLineSignatureError("Invalid LINE signature") from error

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            handle_text_message(
                line_id=event.source.user_id,
                reply_token=event.reply_token,
                text=event.message.text,
            )
    return api_success({"status": "ok"})
