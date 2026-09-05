"""LINE Login (OAuth 2.0 / OpenID Connect) HTTP calls.

Separate from app.line.client, which talks to the Messaging API channel.
"""

import logging
from urllib.parse import urlencode

import requests
from flask import current_app

from app.shared.errors import LineLoginConfigurationError, LineLoginError

logger = logging.getLogger(__name__)

AUTHORIZATION_ENDPOINT = "https://access.line.me/oauth2/v2.1/authorize"
TOKEN_ENDPOINT = "https://api.line.me/oauth2/v2.1/token"
VERIFY_ENDPOINT = "https://api.line.me/oauth2/v2.1/verify"
PROFILE_ENDPOINT = "https://api.line.me/v2/profile"
DEFAULT_SCOPE = "openid profile"
TIMEOUT_SECONDS = 10


class LineLoginClient:
    """Thin wrapper: authorization URL, token exchange, identity verification."""

    @property
    def channel_id(self):
        return current_app.config.get("LINE_LOGIN_CHANNEL_ID", "")

    @property
    def channel_secret(self):
        return current_app.config.get("LINE_LOGIN_CHANNEL_SECRET", "")

    @property
    def callback_url(self):
        return current_app.config.get("LINE_LOGIN_CALLBACK_URL", "")

    def require_config(self):
        missing = [
            name
            for name, value in (
                ("LINE_LOGIN_CHANNEL_ID", self.channel_id),
                ("LINE_LOGIN_CHANNEL_SECRET", self.channel_secret),
                ("LINE_LOGIN_CALLBACK_URL", self.callback_url),
            )
            if not value
        ]
        if missing:
            raise LineLoginConfigurationError(f"LINE Login is not configured: {', '.join(missing)}")

    def build_authorization_url(self, *, state):
        self.require_config()
        params = {
            "response_type": "code",
            "client_id": self.channel_id,
            "redirect_uri": self.callback_url,
            "state": state,
            "scope": current_app.config.get("LINE_LOGIN_SCOPE") or DEFAULT_SCOPE,
        }
        # Set only when the Login channel is linked to the Official Account and we
        # want the "add as friend" prompt during login.
        bot_prompt = current_app.config.get("LINE_LOGIN_BOT_PROMPT", "")
        if bot_prompt:
            params["bot_prompt"] = bot_prompt
        return f"{AUTHORIZATION_ENDPOINT}?{urlencode(params)}"

    def fetch_identity(self, *, code):
        """Exchange the code and return (line_user_id, display_name, picture_url)."""
        token_payload = self._exchange_code(code=code)

        id_token = token_payload.get("id_token")
        if id_token:
            claims = self._verify_id_token(id_token=id_token)
            return claims["sub"], claims.get("name"), claims.get("picture")

        access_token = token_payload.get("access_token")
        if not access_token:
            raise LineLoginError("LINE token response carried no usable token")
        profile = self._fetch_profile(access_token=access_token)
        return profile["userId"], profile.get("displayName"), profile.get("pictureUrl")

    def _exchange_code(self, *, code):
        self.require_config()
        payload = self._post(
            TOKEN_ENDPOINT,
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": self.callback_url,
                "client_id": self.channel_id,
                "client_secret": self.channel_secret,
            },
            action="token exchange",
        )
        return payload

    def _verify_id_token(self, *, id_token):
        claims = self._post(
            VERIFY_ENDPOINT,
            data={"id_token": id_token, "client_id": self.channel_id},
            action="id_token verification",
        )
        if not claims.get("sub"):
            raise LineLoginError("LINE identity carried no user id")
        return claims

    def _fetch_profile(self, *, access_token):
        try:
            response = requests.get(
                PROFILE_ENDPOINT,
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=TIMEOUT_SECONDS,
            )
        except requests.RequestException as error:
            logger.warning("line login profile request failed: %s", error)
            raise LineLoginError("Could not reach LINE profile API") from error

        if response.status_code != 200:
            logger.warning("line login profile rejected: status=%s", response.status_code)
            raise LineLoginError("LINE rejected the profile request")

        profile = response.json()
        if not profile.get("userId"):
            raise LineLoginError("LINE profile carried no user id")
        return profile

    def _post(self, url, *, data, action):
        try:
            response = requests.post(
                url,
                data=data,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=TIMEOUT_SECONDS,
            )
        except requests.RequestException as error:
            logger.warning("line login %s failed: %s", action, error)
            raise LineLoginError(f"Could not reach LINE during {action}") from error

        if response.status_code != 200:
            # Status only: the body can echo the code and the channel secret back.
            logger.warning("line login %s rejected: status=%s", action, response.status_code)
            raise LineLoginError(f"LINE rejected the {action}")

        return response.json()
