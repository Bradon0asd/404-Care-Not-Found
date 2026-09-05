import json

import pytest

from app.chat.client import GeminiClient
from app.line.client import LineClient
from app.models import CareSchedule, StressEvent, VitalSignLog


COMPANION_REPLY = "Aduh, kamu pasti kaget. Nenek sekarang sudah aman ya. Kamu sudah makan?"


@pytest.fixture()
def chat_app(app):
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
    """Answer each call by what the prompt asks for, and record every prompt sent."""
    state = {
        "prompts": [],
        "system_instructions": [],
        "stress_score": 0.1,
        "extraction": {"schedules": [], "vital_signs": []},
        "reply": COMPANION_REPLY,
        "fail": False,
        "title": "Nenek jatuh",
    }

    def fake_generate(self, prompt, *, system_instruction=None, temperature=0.7, json_mode=False):
        state["prompts"].append(prompt)
        state["system_instructions"].append(system_instruction)
        if state["fail"]:
            from app.shared.errors import GoogleAiApiError

            raise GoogleAiApiError("upstream down")
        if prompt.startswith("Rate the emotional strain"):
            return json.dumps({"score": state["stress_score"]})
        if prompt.startswith("Assess this caregiver's emotional strain"):
            return json.dumps({"score": state["stress_score"], "high_stress": True})
        if prompt.startswith("Extract the objective daily-care facts"):
            return json.dumps(state["extraction"])
        if prompt.startswith("From the patient context"):
            return json.dumps({"care_context": "Nenek 90 tahun, alzheimer."})
        if prompt.startswith("Give this conversation"):
            return json.dumps({"title": state["title"]})
        if prompt.startswith("Write "):
            return json.dumps({"questions": [{"key": "sleep", "text": "Sudah cukup tidur?"}]})
        return state["reply"]

    monkeypatch.setattr(GeminiClient, "generate_content", fake_generate)
    return state


# --- Setup mode -----------------------------------------------------------

def test_setup_stores_the_generated_profile_for_reuse(chat_app, client, model):
    nurse_id, _, recipient_id = _paired_setup(client)

    response = client.post(
        "/api/chat/agent",
        json={"care_recipient_id": recipient_id, "system_prompt": "Nenek 90 tahun."},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 201
    body = response.get_json()["data"]
    # Generated once here so daily chat never pays for it again.
    assert body["generated_profile"] == {"care_context": "Nenek 90 tahun, alzheimer."}
    assert body["baseline_completed_at"] is None


def test_free_tier_allows_one_agent(chat_app, client, model):
    nurse_id, owner_id, recipient_id = _paired_setup(client)
    _create_agent(client, nurse_id, recipient_id)
    other_recipient = _create_recipient(client, nurse_id, name="Kakek")

    response = client.post(
        "/api/chat/agent",
        json={"care_recipient_id": other_recipient, "system_prompt": "Kakek 80 tahun."},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 409
    assert response.get_json()["error"]["code"] == "CARE_AGENT_LIMIT_REACHED"


def test_baseline_questions_never_sound_like_a_test(chat_app, client, model):
    nurse_id, _, recipient_id = _paired_setup(client)
    _create_agent(client, nurse_id, recipient_id)

    response = client.get("/api/chat/agent/baseline", headers=_auth(nurse_id))

    assert response.status_code == 200
    prompt = [p for p in model["prompts"] if p.startswith("Write ")][0]
    banned = "test, assessment, screening, diagnosis, or score"
    assert f"Never use the words {banned}" in prompt
    assert "as chat between friends" in prompt


def test_chat_needs_the_one_off_setup_first(chat_app, client, model):
    nurse_id, _, recipient_id = _paired_setup(client)
    _create_agent(client, nurse_id, recipient_id)

    response = client.post("/api/chat/rooms", json={}, headers=_auth(nurse_id))

    assert response.status_code == 409
    assert response.get_json()["error"]["code"] == "BASELINE_REQUIRED"


# --- Chat mode ------------------------------------------------------------

def test_free_tier_allows_one_room_a_day(chat_app, client, model):
    nurse_id = _ready_nurse(client)
    _open_room(client, nurse_id)

    response = client.post("/api/chat/rooms", json={}, headers=_auth(nurse_id))

    assert response.status_code == 429
    assert response.get_json()["error"]["code"] == "CHAT_ROOM_QUOTA_REACHED"


def test_reply_carries_companionship_and_no_score(chat_app, client, model, pushed_messages):
    nurse_id = _ready_nurse(client)
    room_id = _open_room(client, nurse_id)

    response = client.post(
        f"/api/chat/rooms/{room_id}/messages",
        json={"text": "Nenek jatuh pagi ini."},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 201
    body = response.get_json()["data"]
    assert body["ai_message"]["text"] == COMPANION_REPLY
    # Nothing backstage may appear in what she reads.
    assert set(body["ai_message"]) == {"id", "room_id", "sender", "text", "created_at"}
    assert "stress" not in json.dumps(body).lower()


def test_daily_prompt_stays_short(chat_app, client, model):
    """B3: the cost story depends on not resending the whole history."""
    nurse_id = _ready_nurse(client)
    room_id = _open_room(client, nurse_id)
    for index in range(6):
        client.post(
            f"/api/chat/rooms/{room_id}/messages",
            json={"text": f"pesan-{index}"},
            headers=_auth(nurse_id),
        )

    companion_prompts = [
        prompt
        for prompt in model["prompts"]
        if not prompt.startswith(("Rate", "Assess", "Extract", "From", "Write", "Give"))
    ]
    last = companion_prompts[-1]
    assert "pesan-0" not in last
    assert last.count("user:") <= 6


def test_guardrail_rides_along_with_the_persona(chat_app, client, model):
    """B4: a stored guardrail is useless unless it reaches the model."""
    nurse_id, _, recipient_id = _paired_setup(client)
    client.post(
        "/api/chat/agent",
        json={
            "care_recipient_id": recipient_id,
            "system_prompt": "Nenek 90 tahun.",
            "guardrail": "Jangan pernah menyebut biaya rumah sakit.",
        },
        headers=_auth(nurse_id),
    )
    _complete_baseline(client, nurse_id)
    room_id = _open_room(client, nurse_id)

    client.post(
        f"/api/chat/rooms/{room_id}/messages",
        json={"text": "halo"},
        headers=_auth(nurse_id),
    )

    sent = [text for text in model["system_instructions"] if text]
    assert any("Jangan pernah menyebut biaya rumah sakit." in text for text in sent)
    assert any("contact the family or seek medical care" in text for text in sent)


def test_model_failure_still_returns_a_warm_reply(chat_app, client, model):
    """A2: the conversation must not break in front of an audience."""
    nurse_id = _ready_nurse(client)
    room_id = _open_room(client, nurse_id)
    model["fail"] = True

    response = client.post(
        f"/api/chat/rooms/{room_id}/messages",
        json={"text": "Aku capek sekali."},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 201
    assert "aku di sini" in response.get_json()["data"]["ai_message"]["text"].lower()


def test_another_users_room_is_not_reachable(chat_app, client, model):
    nurse_id = _ready_nurse(client)
    room_id = _open_room(client, nurse_id)
    intruder = _create_user(client, "intruder-line-id", role="nurse")

    response = client.get(f"/api/chat/rooms/{room_id}", headers=_auth(intruder))

    assert response.status_code == 403


# --- The demo mainline, end to end ----------------------------------------

def test_one_indonesian_message_feeds_tab01_and_the_employer_notice(
    chat_app, client, model, pushed_messages
):
    """Grandma fell: one message, three outcomes, and the content stays with her."""
    nurse_id = _ready_nurse(client)
    room_id = _open_room(client, nurse_id, mood_weather="rainy")
    confession = "Nenek jatuh jam 9 pagi, sudah ke rumah sakit. Aku merasa bersalah."
    model["stress_score"] = 0.95
    model["extraction"] = {
        "schedules": [
            {"title": "阿嬤跌倒", "description": "已送醫，醫師確認無大礙", "start_time": "09:00"}
        ],
        "vital_signs": [
            {"vital_type": "blood_pressure", "value": 150, "secondary_value": 90,
             "measured_at": "09:30", "note": "跌倒後量測"}
        ],
    }

    response = client.post(
        f"/api/chat/rooms/{room_id}/messages",
        json={"text": confession},
        headers=_auth(nurse_id),
    )

    # 1. She reads companionship, never a score.
    assert response.status_code == 201
    assert response.get_json()["data"]["ai_message"]["text"] == COMPANION_REPLY

    with chat_app.app_context():
        # 2. The care facts landed in Tab 01, in Chinese.
        schedule = CareSchedule.query.one()
        assert schedule.title == "阿嬤跌倒"
        assert schedule.start_time.strftime("%H:%M") == "09:00"
        vital = VitalSignLog.query.one()
        assert (vital.vital_type, vital.value, vital.secondary_value) == (
            "blood_pressure",
            150,
            90,
        )
        assert vital.unit == "mmHg"
        assert StressEvent.query.count() == 1

    # 3. The employer got a count and a time, and nothing she wrote.
    assert len(pushed_messages) == 1
    notice = pushed_messages[0]["text"]
    assert "異常筆數：1 筆" in notice
    assert confession not in notice
    for word in ("Nenek", "jatuh", "bersalah", "跌倒", "自責"):
        assert word not in notice


def test_extraction_failure_does_not_break_the_reply(chat_app, client, model):
    nurse_id = _ready_nurse(client)
    room_id = _open_room(client, nurse_id)
    # A shape the writer cannot use at all.
    model["extraction"] = {"schedules": [{"description": "no title"}], "vital_signs": [{}]}

    response = client.post(
        f"/api/chat/rooms/{room_id}/messages",
        json={"text": "halo"},
        headers=_auth(nurse_id),
    )

    assert response.status_code == 201
    with chat_app.app_context():
        assert CareSchedule.query.count() == 0
        assert VitalSignLog.query.count() == 0


# --- helpers --------------------------------------------------------------

def _paired_setup(client):
    nurse_id = _create_user(client, "nurse-line-id", role="nurse")
    owner_id = _create_user(client, "owner-line-id", role="owner")
    assert client.post(
        f"/api/users/{owner_id}/pair", json={"pair_user_id": nurse_id}
    ).status_code == 200
    recipient_id = _create_recipient(client, nurse_id)
    return nurse_id, owner_id, recipient_id


def _ready_nurse(client):
    nurse_id, _, recipient_id = _paired_setup(client)
    _create_agent(client, nurse_id, recipient_id)
    _complete_baseline(client, nurse_id)
    return nurse_id


def _create_agent(client, nurse_id, recipient_id):
    response = client.post(
        "/api/chat/agent",
        json={"care_recipient_id": recipient_id, "system_prompt": "Nenek 90 tahun."},
        headers=_auth(nurse_id),
    )
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _complete_baseline(client, nurse_id):
    response = client.post(
        "/api/chat/agent/baseline",
        json={"answers": [{"key": "sleep", "answer": "Kurang tidur."}]},
        headers=_auth(nurse_id),
    )
    assert response.status_code == 200


def _open_room(client, nurse_id, mood_weather=None, title=None):
    payload = {}
    if mood_weather:
        payload["mood_weather"] = mood_weather
    if title:
        payload["title"] = title
    response = client.post("/api/chat/rooms", json=payload, headers=_auth(nurse_id))
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _create_recipient(client, nurse_id, name="Nenek"):
    response = client.post(
        "/api/care-recipients", json={"name": name}, headers=_auth(nurse_id)
    )
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _create_user(client, line_id, *, role):
    response = client.post("/api/users", json={"line_id": line_id, "role": role})
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _auth(user_id):
    return {"X-User-Id": str(user_id)}


# --- Opening a room and naming it ----------------------------------------

def test_room_opens_with_a_greeting_that_names_who_she_cares_for(chat_app, client, model):
    """She never lands on an empty screen (PRD: 聊天室開頭帶入歡迎語 + 照顧者資訊)."""
    nurse_id = _ready_nurse(client)
    room_id = _open_room(client, nurse_id)

    response = client.get(f"/api/chat/rooms/{room_id}", headers=_auth(nurse_id))

    messages = response.get_json()["data"]["messages"]
    assert len(messages) == 1
    greeting = messages[0]
    assert greeting["sender"] == "ai"
    assert "404: Care Not Found" in greeting["text"]
    # The patient's name and stored summary are both in it.
    assert "Nenek" in greeting["text"]
    assert "Nenek 90 tahun, alzheimer." in greeting["text"]


def test_greeting_needs_no_model_call(chat_app, client, model):
    """Written, not generated: it must still appear when the model is down."""
    nurse_id = _ready_nurse(client)
    model["fail"] = True
    model["prompts"].clear()

    room_id = _open_room(client, nurse_id)

    assert model["prompts"] == []
    response = client.get(f"/api/chat/rooms/{room_id}", headers=_auth(nurse_id))
    assert "404: Care Not Found" in response.get_json()["data"]["messages"][0]["text"]


def test_agent_exposes_the_patient_name(chat_app, client, model):
    nurse_id = _ready_nurse(client)

    response = client.get("/api/chat/agent", headers=_auth(nurse_id))

    assert response.get_json()["data"]["care_recipient_name"] == "Nenek"


def test_first_message_names_an_unnamed_room(chat_app, client, model):
    nurse_id = _ready_nurse(client)
    room_id = _open_room(client, nurse_id)
    model["title"] = "Nenek jatuh"

    client.post(
        f"/api/chat/rooms/{room_id}/messages",
        json={"text": "Nenek jatuh pagi ini."},
        headers=_auth(nurse_id),
    )

    listed = client.get("/api/chat/rooms", headers=_auth(nurse_id)).get_json()["data"]
    assert listed[0]["title"] == "Nenek jatuh"


def test_a_room_she_named_is_left_alone(chat_app, client, model):
    nurse_id = _ready_nurse(client)
    room_id = _open_room(client, nurse_id, title="Judul saya")
    model["title"] = "Nenek jatuh"

    client.post(
        f"/api/chat/rooms/{room_id}/messages",
        json={"text": "Nenek jatuh pagi ini."},
        headers=_auth(nurse_id),
    )

    listed = client.get("/api/chat/rooms", headers=_auth(nurse_id)).get_json()["data"]
    assert listed[0]["title"] == "Judul saya"
    assert not [p for p in model["prompts"] if p.startswith("Give this conversation")]


def test_mood_weather_reaches_the_analysis(chat_app, client, model):
    """B6: the one-tap weather is an input to the reading, not just a stored value."""
    nurse_id = _ready_nurse(client)
    room_id = _open_room(client, nurse_id, mood_weather="storm")

    client.post(
        f"/api/chat/rooms/{room_id}/messages",
        json={"text": "hari ini berat"},
        headers=_auth(nurse_id),
    )

    triage = [p for p in model["prompts"] if p.startswith("Rate the emotional strain")][0]
    assert "storm" in triage
