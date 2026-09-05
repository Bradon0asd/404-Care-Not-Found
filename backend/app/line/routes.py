import logging

from flask import current_app, request
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.webhook import WebhookParser
from linebot.v3.webhooks import MessageEvent, TextMessageContent

from app.auth.current_user import get_current_user
from app.shared.errors import InvalidLineSignatureError, LineConfigurationError
from app.shared.response import api_success
from app.line import line_bp
from app.line.notifications import notify_stress_signal
from app.line.schemas import StressSignalCreateSchema, StressSignalSchema
from app.line.service import handle_text_message
from app.models.diary import utc_now


logger = logging.getLogger(__name__)


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
        # Lengths only: a channel secret is 32 chars, so a mismatch shows up here
        # without ever writing the secret itself to the logs.
        logger.warning(
            "line signature rejected: secret_chars=%s signature_chars=%s body_bytes=%s",
            len(secret),
            len(signature),
            len(body),
        )
        raise InvalidLineSignatureError("Invalid LINE signature") from error

    logger.info("line webhook received: events=%s", len(events))

    for event in events:
        if isinstance(event, MessageEvent) and isinstance(event.message, TextMessageContent):
            handle_text_message(
                line_id=event.source.user_id,
                reply_token=event.reply_token,
                text=event.message.text,
            )
    return api_success({"status": "ok"})


@line_bp.post("/stress-signals")
@line_bp.arguments(StressSignalCreateSchema, location="json")
@line_bp.doc(
    summary="Notify the paired owner that records need attention",
    security=[{"UserIdHeader": []}],
)
def create_stress_signal(args):
    occurred_at = args["occurred_at"] or utc_now()
    owner = notify_stress_signal(
        nurse=get_current_user(),
        abnormal_count=args["abnormal_count"],
        occurred_at=occurred_at,
    )
    return api_success(
        StressSignalSchema().dump(
            {
                "owner_id": owner.id,
                "abnormal_count": args["abnormal_count"],
                "occurred_at": occurred_at,
            }
        ),
        status_code=202,
    )
