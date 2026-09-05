from unittest.mock import MagicMock, patch
import pytest
import requests

from app.chat.client import GeminiClient
from app.shared.errors import GoogleAiApiError, GoogleAiConfigurationError


def test_gemini_client_missing_key_raises(app):
    app.config["GEMINI_API_KEY"] = ""
    client = GeminiClient()
    with pytest.raises(GoogleAiConfigurationError):
        client.generate_content("hello")


def test_gemini_client_successful_response(app):
    app.config["GEMINI_API_KEY"] = "test-api-key"
    app.config["GEMINI_BASE_URL"] = "https://generativelanguage.googleapis.com/v1beta"
    app.config["GEMINI_MODEL"] = "gemini-1.5-flash"

    mock_response = MagicMock()
    mock_response.ok = True
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "candidates": [
            {
                "content": {
                    "parts": [{"text": "Halo! Saya di sini untuk menemani Anda."}]
                },
                "finishReason": "STOP",
            }
        ]
    }

    with patch("requests.post", return_value=mock_response) as mock_post:
        client = GeminiClient()
        result = client.generate_content(
            "Halo apa kabar",
            system_instruction="Kamu adalah teman yang hangat.",
            temperature=0.4,
            json_mode=False,
        )

        assert result == "Halo! Saya di sini untuk menemani Anda."
        mock_post.assert_called_once()
        call_args, call_kwargs = mock_post.call_args
        assert call_args[0] == "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        assert call_kwargs["headers"]["x-goog-api-key"] == "test-api-key"
        assert call_kwargs["json"]["contents"][0]["parts"][0]["text"] == "Halo apa kabar"
        assert call_kwargs["json"]["systemInstruction"]["parts"][0]["text"] == "Kamu adalah teman yang hangat."
        assert call_kwargs["json"]["generationConfig"]["temperature"] == 0.4


def test_gemini_client_api_error(app):
    app.config["GEMINI_API_KEY"] = "test-api-key"

    mock_response = MagicMock()
    mock_response.ok = False
    mock_response.status_code = 400
    mock_response.text = "Bad Request"
    mock_response.json.return_value = {"error": {"message": "Invalid argument"}}

    with patch("requests.post", return_value=mock_response):
        client = GeminiClient()
        with pytest.raises(GoogleAiApiError) as exc_info:
            client.generate_content("hello")
        assert "Invalid argument" in str(exc_info.value)


def test_gemini_client_network_error(app):
    app.config["GEMINI_API_KEY"] = "test-api-key"

    with patch("requests.post", side_effect=requests.RequestException("Connection refused")):
        client = GeminiClient()
        with pytest.raises(GoogleAiApiError) as exc_info:
            client.generate_content("hello")
        assert "Network error" in str(exc_info.value)
