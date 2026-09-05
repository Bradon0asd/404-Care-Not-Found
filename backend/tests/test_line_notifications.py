import pytest

from app.line.client import LineClient


@pytest.fixture()
def line_app(app):
    app.config["LINE_CHANNEL_ACCESS_TOKEN"] = "test-access-token"
    return app


@pytest.fixture()
def pushed_messages(monkeypatch):
    messages = []

    def fake_push_text(self, *, user_id, text):
        messages.append({"user_id": user_id, "text": text})

    monkeypatch.setattr(LineClient, "push_text", fake_push_text)
    return messages


def test_stress_signal_reaches_the_paired_owner(line_app, client, pushed_messages):
    nurse_id, _ = _paired_nurse_and_owner(client)

    response = client.post(
        "/api/line/stress-signals",
        json={"abnormal_count": 3, "occurred_at": "2026-09-05T14:30:00"},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 202
    assert len(pushed_messages) == 1
    assert pushed_messages[0]["user_id"] == "owner-line-id"
    assert "異常筆數：3 筆" in pushed_messages[0]["text"]
    assert "時間點：14:30" in pushed_messages[0]["text"]


def test_stress_signal_refuses_to_carry_content(line_app, client, pushed_messages):
    """The owner is told a signal fired, never what the nurse wrote."""
    nurse_id, _ = _paired_nurse_and_owner(client)

    response = client.post(
        "/api/line/stress-signals",
        json={"abnormal_count": 1, "content": "阿嬤跌倒了，我很自責"},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 422
    assert pushed_messages == []


def test_stress_signal_message_only_holds_count_time_and_advice(line_app, client, pushed_messages):
    nurse_id, _ = _paired_nurse_and_owner(client)

    client.post(
        "/api/line/stress-signals",
        json={"abnormal_count": 2, "occurred_at": "2026-09-05T09:00:00"},
        headers=_auth(nurse_id),
    )

    assert pushed_messages[0]["text"].splitlines() == [
        "【0905】【壓力告知】通知內容",
        "本日看護壓力偵測異常筆數：2 筆",
        "時間點：09:00",
        "建議關心一下看護今日心理狀況",
        "友善職場 從你我的關心開始！",
    ]


def test_stress_signal_defaults_to_now(line_app, client, pushed_messages):
    nurse_id, _ = _paired_nurse_and_owner(client)

    response = client.post(
        "/api/line/stress-signals",
        json={"abnormal_count": 2},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 202
    assert response.get_json()["data"]["occurred_at"] is not None


def test_stress_signal_requires_a_paired_owner(line_app, client, pushed_messages):
    nurse_id = _create_user(client, "lonely-nurse", role="nurse")

    response = client.post(
        "/api/line/stress-signals",
        json={"abnormal_count": 1},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 400
    assert response.get_json()["error"]["code"] == "LINE_RECIPIENT_NOT_PAIRED"
    assert pushed_messages == []


def test_owner_cannot_raise_a_stress_signal(line_app, client, pushed_messages):
    _, owner_id = _paired_nurse_and_owner(client)

    response = client.post(
        "/api/line/stress-signals",
        json={"abnormal_count": 1},
        headers=_auth(owner_id),
    )

    assert response.status_code == 403
    assert response.get_json()["error"]["code"] == "PERMISSION_DENIED"
    assert pushed_messages == []


def test_stress_signal_validates_count(line_app, client, pushed_messages):
    nurse_id, _ = _paired_nurse_and_owner(client)

    response = client.post(
        "/api/line/stress-signals",
        json={"abnormal_count": 0},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 422
    assert pushed_messages == []


def _paired_nurse_and_owner(client):
    nurse_id = _create_user(client, "nurse-line-id", role="nurse")
    owner_id = _create_user(client, "owner-line-id", role="owner")
    response = client.post(
        f"/api/users/{owner_id}/pair",
        json={"pair_user_id": nurse_id},
    )
    assert response.status_code == 200
    return nurse_id, owner_id


def _create_user(client, line_id, *, role):
    response = client.post(
        "/api/users",
        json={"line_id": line_id, "role": role},
    )
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _auth(user_id):
    return {"X-User-Id": str(user_id)}
