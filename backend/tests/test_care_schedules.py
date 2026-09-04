from app.extensions import db
from app.models import CareRecipient, User, UserRole


def test_schedule_crud_and_sorting(client, app):
    owner_id, nurse_id, recipient_id = _create_care_context(app, "sched")

    created = client.post(
        f"/api/care-recipients/{recipient_id}/schedules",
        headers=_headers(nurse_id),
        json={
            "schedule_type": "weekday",
            "weekday": 0,
            "start_time": "13:00",
            "title": "復健",
            "description": "午餐後",
        },
    )
    assert created.status_code == 201
    schedule = created.get_json()["data"]
    assert schedule["care_recipient_id"] == recipient_id
    assert schedule["creator_id"] == nurse_id
    assert schedule["start_time"] == "13:00"

    _create_schedule(client, owner_id, recipient_id, weekday=0, start_time="09:00", title="吃胃藥")
    _create_schedule(client, owner_id, recipient_id, schedule_type="weekend", weekday=6, start_time="10:00")

    listed = client.get(
        f"/api/care-recipients/{recipient_id}/schedules",
        headers=_headers(owner_id),
    )
    assert listed.status_code == 200
    items = listed.get_json()["data"]
    assert [(item["weekday"], item["start_time"]) for item in items] == [
        (0, "09:00"),
        (0, "13:00"),
        (6, "10:00"),
    ]

    filtered = client.get(
        f"/api/care-recipients/{recipient_id}/schedules?schedule_type=weekend",
        headers=_headers(owner_id),
    )
    assert filtered.status_code == 200
    assert [item["schedule_type"] for item in filtered.get_json()["data"]] == ["weekend"]

    updated = client.patch(
        f"/api/schedules/{schedule['id']}",
        headers=_headers(owner_id),
        json={"start_time": "09:30", "title": "吃胃藥"},
    )
    assert updated.status_code == 200
    assert updated.get_json()["data"]["start_time"] == "09:30"
    assert updated.get_json()["data"]["title"] == "吃胃藥"

    deleted = client.delete(f"/api/schedules/{schedule['id']}", headers=_headers(nurse_id))
    assert deleted.status_code == 200

    missing = client.get(f"/api/schedules/{schedule['id']}", headers=_headers(nurse_id))
    assert missing.status_code == 404
    assert missing.get_json()["error"]["code"] == "CARE_SCHEDULE_NOT_FOUND"


def test_schedule_requires_recipient_access(client, app):
    _, nurse_id, recipient_id = _create_care_context(app, "sched-perm")
    stranger_id = _create_user(client, "sched-stranger")

    listed = client.get(
        f"/api/care-recipients/{recipient_id}/schedules",
        headers=_headers(stranger_id),
    )
    assert listed.status_code == 403
    assert listed.get_json()["error"]["code"] == "PERMISSION_DENIED"

    schedule_id = _create_schedule(client, nurse_id, recipient_id)
    blocked = client.patch(
        f"/api/schedules/{schedule_id}",
        headers=_headers(stranger_id),
        json={"title": "changed"},
    )
    assert blocked.status_code == 403

    unknown = client.get("/api/care-recipients/9999/schedules", headers=_headers(nurse_id))
    assert unknown.status_code == 404
    assert unknown.get_json()["error"]["code"] == "CARE_RECIPIENT_NOT_FOUND"


def test_schedule_create_validates_input(client, app):
    _, nurse_id, recipient_id = _create_care_context(app, "sched-validate")

    bad_type = client.post(
        f"/api/care-recipients/{recipient_id}/schedules",
        headers=_headers(nurse_id),
        json={"schedule_type": "monthly", "weekday": 0, "start_time": "09:00", "title": "x"},
    )
    assert bad_type.status_code == 422

    bad_weekday = client.post(
        f"/api/care-recipients/{recipient_id}/schedules",
        headers=_headers(nurse_id),
        json={"schedule_type": "weekday", "weekday": 7, "start_time": "09:00", "title": "x"},
    )
    assert bad_weekday.status_code == 422

    server_controlled = client.post(
        f"/api/care-recipients/{recipient_id}/schedules",
        headers=_headers(nurse_id),
        json={
            "schedule_type": "weekday",
            "weekday": 0,
            "start_time": "09:00",
            "title": "x",
            "creator_id": 999,
        },
    )
    assert server_controlled.status_code == 422


def _create_schedule(
    client,
    user_id,
    recipient_id,
    *,
    schedule_type="weekday",
    weekday=0,
    start_time="09:00",
    title="吃胃藥",
):
    response = client.post(
        f"/api/care-recipients/{recipient_id}/schedules",
        headers=_headers(user_id),
        json={
            "schedule_type": schedule_type,
            "weekday": weekday,
            "start_time": start_time,
            "title": title,
        },
    )
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _create_care_context(app, prefix):
    with app.app_context():
        owner = User(line_id=f"{prefix}-owner", role=UserRole.OWNER.value)
        nurse = User(line_id=f"{prefix}-nurse", role=UserRole.NURSE.value)
        recipient = CareRecipient(name="阿嬤", owner=owner, nurse=nurse)
        db.session.add(recipient)
        db.session.commit()
        return owner.id, nurse.id, recipient.id


def _create_user(client, line_id, *, role="nurse"):
    response = client.post("/api/users", json={"line_id": line_id, "role": role})
    assert response.status_code == 201
    return response.get_json()["data"]["id"]


def _headers(user_id):
    return {"X-User-Id": str(user_id)}
