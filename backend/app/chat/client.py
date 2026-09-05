import logging
import requests
from flask import current_app

from app.shared.errors import GoogleAiApiError, GoogleAiConfigurationError

logger = logging.getLogger(__name__)


class GeminiClient:
    def __init__(self, api_key=None, base_url=None, model=None):
        self._explicit_api_key = api_key
        self._explicit_base_url = base_url
        self._explicit_model = model

    @property
    def api_key(self):
        if self._explicit_api_key:
            return self._explicit_api_key
        return current_app.config.get("GEMINI_API_KEY", "")

    @property
    def base_url(self):
        url = self._explicit_base_url or current_app.config.get("GEMINI_BASE_URL")
        return (url or "https://generativelanguage.googleapis.com/v1beta").rstrip("/")

    @property
    def model(self):
        return (
            self._explicit_model
            or current_app.config.get("GEMINI_MODEL")
            or "gemini-3.6-flash"
        )

    def generate_content(
        self,
        prompt,
        *,
        system_instruction=None,
        temperature=0.7,
        json_mode=False,
    ):
        key = self.api_key
        if not key:
            raise GoogleAiConfigurationError("Google AI API key is not configured")

        endpoint = f"{self.base_url}/models/{self.model}:generateContent"
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": key,
        }
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": prompt}],
                }
            ],
            "generationConfig": {
                "temperature": temperature,
            },
        }

        if system_instruction:
            payload["systemInstruction"] = {
                "parts": [{"text": system_instruction}],
            }

        if json_mode:
            payload["generationConfig"]["responseMimeType"] = "application/json"

        try:
            response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
        except requests.RequestException as e:
            logger.error("Gemini API request failed: %s", e)
            raise GoogleAiApiError(f"Network error calling Google AI: {e}") from e

        if not response.ok:
            logger.error("Gemini API returned %s: %s", response.status_code, response.text)
            try:
                err_data = response.json().get("error", {})
                msg = err_data.get("message") or response.text
            except Exception:
                msg = response.text
            raise GoogleAiApiError(f"Google AI API error ({response.status_code}): {msg}")

        data = response.json()
        candidates = data.get("candidates", [])
        if not candidates:
            raise GoogleAiApiError("Google AI returned no candidates")

        parts = candidates[0].get("content", {}).get("parts", [])
        # Gemini 3.x can put a thought part first, so join every part that carries text
        # instead of trusting parts[0].
        text = "".join(part.get("text", "") for part in parts)
        if not text:
            raise GoogleAiApiError("Google AI response contained no text")

        return text
