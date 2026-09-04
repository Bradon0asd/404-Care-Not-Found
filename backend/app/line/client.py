from flask import current_app
from linebot.v3.messaging import (
    ApiClient,
    Configuration,
    MessagingApi,
    PushMessageRequest,
    ReplyMessageRequest,
    TextMessage,
)

from app.common.errors import LineConfigurationError


class LineClient:
    def _messaging_api(self):
        token = current_app.config["LINE_CHANNEL_ACCESS_TOKEN"]
        if not token:
            raise LineConfigurationError("LINE channel access token is not configured")
        api_client = ApiClient(Configuration(access_token=token))
        return api_client, MessagingApi(api_client)

    def reply_text(self, *, reply_token, text):
        api_client, api = self._messaging_api()
        try:
            api.reply_message(
                ReplyMessageRequest(
                    reply_token=reply_token,
                    messages=[TextMessage(text=text)],
                )
            )
        finally:
            api_client.close()

    def push_text(self, *, user_id, text):
        api_client, api = self._messaging_api()
        try:
            api.push_message(
                PushMessageRequest(
                    to=user_id,
                    messages=[TextMessage(text=text)],
                )
            )
        finally:
            api_client.close()
