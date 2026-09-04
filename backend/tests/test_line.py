import base64
import hashlib
import hmac
import json

import pytest

from app.line.client import LineClient


SECRET = "test-channel-secret"


def _signed_post(client, body, *, secret=SECRET):
    signature = base64.b64encode(
        hmac.new(secret.encode(), body.encode(), hashlib.sha256).digest()
    ).decode()
    return client.post(
        "/api/line/webhook",
        data=body,
        content_type="application/json",
        headers={"X-Line-Signature": signature},
    )


def _text_message_body(*, line_id="U-line-id", text="halo", reply_token="reply-token"):
    return json.dumps(
        {
            "destination": "Udestination",
            "events": [
                {
                    "type": "message",
                    "mode": "active",
                    "timestamp": 1757000000000,
                    "source": {"type": "user", "userId": line_id},
                    "webhookEventId": "01H0000000000000000000000",
                    "deliveryContext": {"isRedelivery": False},
                    "replyToken": reply_token,
                    "message": {
                        "id": "1",
                        "type": "text",
                        "text": text,
                        "quoteToken": "quote-token",
                    },
                }
            ],
        }
    )


@pytest.fixture()
def line_app(app):
    app.config["LINE_CHANNEL_SECRET"] = SECRET
    app.config["LINE_CHANNEL_ACCESS_TOKEN"] = "test-access-token"
    return app


@pytest.fixture()
def sent_replies(monkeypatch):
    replies = []

    def fake_reply_text(self, *, reply_token, text):
        replies.append({"reply_token": reply_token, "text": text})

    monkeypatch.setattr(LineClient, "reply_text", fake_reply_text)
    return replies


def test_webhook_requires_configured_secret(client):
    response = _signed_post(client, _text_message_body())

    assert response.status_code == 503
    body = response.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "LINE_NOT_CONFIGURED"


def test_webhook_rejects_invalid_signature(line_app, client):
    response = _signed_post(client, _text_message_body(), secret="wrong-secret")

    assert response.status_code == 400
    body = response.get_json()
    assert body["success"] is False
    assert body["error"]["code"] == "INVALID_LINE_SIGNATURE"


def test_webhook_echoes_text_message(line_app, client, sent_replies):
    response = _signed_post(client, _text_message_body(text="halo"))

    assert response.status_code == 200
    assert response.get_json() == {"success": True, "data": {"status": "ok"}}
    assert sent_replies == [{"reply_token": "reply-token", "text": "收到：halo"}]


def test_webhook_registers_unknown_sender(line_app, client, sent_replies):
    from app.models import User

    _signed_post(client, _text_message_body(line_id="U-new-nurse"))

    with line_app.app_context():
        user = User.query.filter_by(line_id="U-new-nurse").first()
        assert user is not None
        assert user.role == "nurse"


def test_webhook_ignores_non_text_events(line_app, client, sent_replies):
    body = json.dumps(
        {
            "destination": "Udestination",
            "events": [
                {
                    "type": "follow",
                    "mode": "active",
                    "timestamp": 1757000000000,
                    "source": {"type": "user", "userId": "U-follower"},
                    "webhookEventId": "01H0000000000000000000001",
                    "deliveryContext": {"isRedelivery": False},
                    "replyToken": "follow-token",
                }
            ],
        }
    )

    response = _signed_post(client, body)

    assert response.status_code == 200
    assert sent_replies == []
