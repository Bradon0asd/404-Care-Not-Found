import json

import pytest

from app.chat.client import GeminiClient
from app.extensions import db
from app.line.client import LineClient
from app.models import Diary, DiaryAiAnalysis, StressEvent


CONFESSION = "Aku menangis sendirian tadi malam. Rasanya tidak sanggup lagi."


@pytest.fixture()
def diary_app(app):
    app.config["GEMINI_API_KEY"] = "test-key"
    app.config["LINE_CHANNEL_ACCESS_TOKEN"] = "test-access-token"
    return app


@pytest.fixture()
def pushed_messages(monkeypatch):
    messages = []

    def fake_push_text(self, *, user_id, text):
        messages.append({"user_id": user_id, "text": text})

    monkeypatch.setattr(LineClient, "push_text", fake_push_text)
    return messages


@pytest.fixture()
def model(monkeypatch):
    state = {"prompts": [], "score": 0.95}

    def fake_generate(self, prompt, *, system_instruction=None, temperature=0.7, json_mode=False):
        state["prompts"].append(prompt)
        if prompt.startswith("Rate the emotional strain"):
            return json.dumps({"score": state["score"]})
        return json.dumps({"score": state["score"], "high_stress": state["score"] >= 0.7})

    monkeypatch.setattr(GeminiClient, "generate_content", fake_generate)
    return state


def test_private_diary_raises_a_signal(diary_app, client, model, pushed_messages):
    nurse_id = _paired_nurse(client)

    response = client.post(
        "/api/diaries",
        json={"content": CONFESSION, "is_private": True},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 201
    with diary_app.app_context():
        assert StressEvent.query.count() == 1
        assert Diary.query.one().ai_analysis == DiaryAiAnalysis.EMERGENCY.value
    assert "異常筆數：1 筆" in pushed_messages[0]["text"]


def test_shared_diary_is_never_read(diary_app, client, model, pushed_messages):
    """A diary she chose to share is not her unguarded voice, so it stays unread."""
    nurse_id = _paired_nurse(client)

    response = client.post(
        "/api/diaries",
        json={"content": CONFESSION, "is_private": False},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 201
    # Not analysed at all: no model call, no signal, no notice.
    assert model["prompts"] == []
    with diary_app.app_context():
        assert StressEvent.query.count() == 0
    assert pushed_messages == []


def test_diary_defaults_to_private_and_is_read(diary_app, client, model, pushed_messages):
    """`is_private` defaults to true, so the default path is the detected one."""
    nurse_id = _paired_nurse(client)

    client.post("/api/diaries", json={"content": CONFESSION}, headers=_auth(nurse_id))

    with diary_app.app_context():
        assert Diary.query.one().is_private is True
        assert StressEvent.query.count() == 1


def test_calm_private_diary_is_marked_normal(diary_app, client, model, pushed_messages):
    nurse_id = _paired_nurse(client)
    model["score"] = 0.1

    client.post(
        "/api/diaries",
        json={"content": "Hari ini tenang, nenek makan dengan baik."},
        headers=_auth(nurse_id),
    )

    with diary_app.app_context():
        assert Diary.query.one().ai_analysis == DiaryAiAnalysis.NORMAL.value
        assert StressEvent.query.count() == 0
    assert pushed_messages == []


def test_notice_carries_no_word_of_the_diary(diary_app, client, model, pushed_messages):
    nurse_id = _paired_nurse(client)

    client.post(
        "/api/diaries",
        json={"content": CONFESSION, "is_private": True},
        headers=_auth(nurse_id),
    )

    notice = pushed_messages[0]["text"]
    assert CONFESSION not in notice
    for word in ("menangis", "sendirian", "sanggup"):
        assert word not in notice


def test_diary_response_never_exposes_the_analysis(diary_app, client, model, pushed_messages):
    """Stress is backstage language; the caregiver's own diary must not show a verdict."""
    nurse_id = _paired_nurse(client)

    response = client.post(
        "/api/diaries",
        json={"content": CONFESSION, "is_private": True},
        headers=_auth(nurse_id),
    )
    listed = client.get("/api/diaries", headers=_auth(nurse_id))

    assert "ai_analysis" not in response.get_json()["data"]
    assert "ai_analysis" not in json.dumps(listed.get_json())
    assert "emergency" not in json.dumps(listed.get_json())


def test_detection_failure_still_saves_the_diary(diary_app, client, monkeypatch):
    """Her entry is never lost to a backstage failure."""
    from app.diaries import service

    def explode(**kwargs):
        raise RuntimeError("analysis exploded")

    monkeypatch.setattr(service.stress_signals, "analyze_and_record", explode)
    nurse_id = _paired_nurse(client)

    response = client.post(
        "/api/diaries",
        json={"content": CONFESSION, "is_private": True},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 201
    with diary_app.app_context():
        assert Diary.query.one().content == CONFESSION


def test_diary_and_chat_signals_share_one_daily_count(diary_app, client, model, pushed_messages):
    """Both paths feed the same count, so the employer sees one running total."""
    nurse_id = _paired_nurse(client)

    for _ in range(2):
        client.post(
            "/api/diaries",
            json={"content": CONFESSION, "is_private": True},
            headers=_auth(nurse_id),
        )

    assert "異常筆數：1 筆" in pushed_messages[0]["text"]
    assert "異常筆數：2 筆" in pushed_messages[1]["text"]
    with diary_app.app_context():
        assert {event.source for event in StressEvent.query.all()} == {"diary"}


def _paired_nurse(client):
    nurse_id = _create_user(client, "nurse-line-id", role="nurse")
    owner_id = _create_user(client, "owner-line-id", role="owner")
    assert client.post(
        f"/api/users/{owner_id}/pair", json={"pair_user_id": nurse_id}, headers=_auth(owner_id)
    ).status_code == 200
    return nurse_id


def _create_user(client, line_id, *, role):
    response = client.post("/api/users", json={"line_id": line_id, "role": role})
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _auth(user_id):
    return {"X-User-Id": str(user_id)}
