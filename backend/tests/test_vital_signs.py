from datetime import datetime, timedelta, timezone

from app.extensions import db
from app.models import CareRecipient, User, UserRole
from app.vital_signs import dashboard_service


def test_vital_sign_create_sets_unit_and_lists_history(client, app):
    owner_id, nurse_id, recipient_id = _create_care_context(app, "vital")

    created = client.post(
        f"/api/care-recipients/{recipient_id}/vital-signs",
        headers=_headers(nurse_id),
        json={
            "vital_type": "blood_pressure",
            "value": 120,
            "secondary_value": 70,
            "measured_at": "2026-09-04T09:30:00",
        },
    )
    assert created.status_code == 201
    log = created.get_json()["data"]
    assert log["unit"] == "mmHg"
    assert log["value"] == 120
    assert log["secondary_value"] == 70
    assert log["creator_id"] == nurse_id

    _create_vital_sign(client, nurse_id, recipient_id, "blood_glucose", 80, "2026-09-03T08:00:00")
    _create_vital_sign(client, nurse_id, recipient_id, "blood_glucose", 90, "2026-09-04T08:00:00")

    listed = client.get(
        f"/api/care-recipients/{recipient_id}/vital-signs",
        headers=_headers(owner_id),
    )
    assert listed.status_code == 200
    items = listed.get_json()["data"]
    assert len(items) == 3
    assert items[0]["measured_at"] >= items[-1]["measured_at"]

    filtered = client.get(
        f"/api/care-recipients/{recipient_id}/vital-signs?vital_type=blood_glucose",
        headers=_headers(owner_id),
    )
    assert [item["value"] for item in filtered.get_json()["data"]] == [90, 80]
    assert all(item["unit"] == "mg/dL" for item in filtered.get_json()["data"])

    ranged = client.get(
        f"/api/care-recipients/{recipient_id}/vital-signs"
        "?vital_type=blood_glucose&start_date=2026-09-04&end_date=2026-09-04",
        headers=_headers(owner_id),
    )
    assert [item["value"] for item in ranged.get_json()["data"]] == [90]


def test_vital_sign_rejects_client_controlled_unit_and_bad_secondary_value(client, app):
    _, nurse_id, recipient_id = _create_care_context(app, "vital-validate")

    bad_unit = client.post(
        f"/api/care-recipients/{recipient_id}/vital-signs",
        headers=_headers(nurse_id),
        json={
            "vital_type": "heart_rate",
            "value": 80,
            "measured_at": "2026-09-04T09:30:00",
            "unit": "whatever",
        },
    )
    assert bad_unit.status_code == 422

    missing_secondary = client.post(
        f"/api/care-recipients/{recipient_id}/vital-signs",
        headers=_headers(nurse_id),
        json={
            "vital_type": "blood_pressure",
            "value": 120,
            "measured_at": "2026-09-04T09:30:00",
        },
    )
    assert missing_secondary.status_code == 422

    unexpected_secondary = client.post(
        f"/api/care-recipients/{recipient_id}/vital-signs",
        headers=_headers(nurse_id),
        json={
            "vital_type": "heart_rate",
            "value": 80,
            "secondary_value": 70,
            "measured_at": "2026-09-04T09:30:00",
        },
    )
    assert unexpected_secondary.status_code == 422

    bad_type = client.post(
        f"/api/care-recipients/{recipient_id}/vital-signs",
        headers=_headers(nurse_id),
        json={"vital_type": "mood", "value": 1, "measured_at": "2026-09-04T09:30:00"},
    )
    assert bad_type.status_code == 422


def test_vital_sign_requires_recipient_access(client, app):
    _, _, recipient_id = _create_care_context(app, "vital-perm")
    stranger_id = _create_user(client, "vital-stranger")

    listed = client.get(
        f"/api/care-recipients/{recipient_id}/vital-signs",
        headers=_headers(stranger_id),
    )
    assert listed.status_code == 403

    dashboard = client.get(
        f"/api/care-recipients/{recipient_id}/dashboard",
        headers=_headers(stranger_id),
    )
    assert dashboard.status_code == 403


def test_dashboard_reports_latest_averages_and_difference(client, app):
    _, nurse_id, recipient_id = _create_care_context(app, "dash")
    now = datetime.now(timezone.utc).replace(tzinfo=None)

    # Current period: the last 7 days.
    _create_vital_sign(client, nurse_id, recipient_id, "blood_glucose", 90, now - timedelta(days=1))
    _create_vital_sign(client, nurse_id, recipient_id, "blood_glucose", 70, now - timedelta(days=2))
    # Previous period: the 7 days before that.
    _create_vital_sign(client, nurse_id, recipient_id, "blood_glucose", 60, now - timedelta(days=8))
    _create_vital_sign(client, nurse_id, recipient_id, "blood_glucose", 80, now - timedelta(days=9))

    _create_vital_sign(
        client,
        nurse_id,
        recipient_id,
        "blood_pressure",
        120,
        now - timedelta(days=1),
        secondary_value=70,
    )
    _create_vital_sign(
        client,
        nurse_id,
        recipient_id,
        "blood_pressure",
        130,
        now - timedelta(days=8),
        secondary_value=76,
    )

    response = client.get(
        f"/api/care-recipients/{recipient_id}/dashboard",
        headers=_headers(nurse_id),
    )
    assert response.status_code == 200
    data = response.get_json()["data"]

    glucose = data["blood_glucose"]
    assert glucose["unit"] == "mg/dL"
    assert glucose["latest"]["value"] == 90
    assert glucose["current_average"]["value"] == 80
    assert glucose["previous_average"]["value"] == 70
    assert glucose["difference"]["value"] == 10
    assert glucose["change_text"] == "較前期增加 10"

    pressure = data["blood_pressure"]
    assert pressure["latest"]["value"] == 120
    assert pressure["latest"]["secondary_value"] == 70
    assert pressure["difference"] == {"value": -10, "secondary_value": -6}
    assert pressure["change_text"] == "收縮壓較前期減少 10，舒張壓較前期減少 6"

    # Types without logs stay empty instead of being invented.
    assert data["temperature"]["latest"] is None
    assert data["temperature"]["current_average"] is None
    assert data["temperature"]["difference"] is None
    assert data["temperature"]["change_text"] is None

    # No medical judgement is ever returned.
    assert "status" not in glucose
    assert "diagnosis" not in glucose


def test_dashboard_periods_are_day_aligned_and_adjacent():
    period = dashboard_service.build_periods(datetime(2026, 9, 4, 15, 30))

    assert period["current_start"] == datetime(2026, 8, 29)
    assert period["current_end"] == datetime(2026, 9, 5)
    assert period["previous_start"] == datetime(2026, 8, 22)
    assert period["previous_end"] == datetime(2026, 8, 29)


def _create_vital_sign(
    client,
    user_id,
    recipient_id,
    vital_type,
    value,
    measured_at,
    *,
    secondary_value=None,
):
    payload = {
        "vital_type": vital_type,
        "value": value,
        "measured_at": measured_at if isinstance(measured_at, str) else measured_at.isoformat(),
    }
    if secondary_value is not None:
        payload["secondary_value"] = secondary_value

    response = client.post(
        f"/api/care-recipients/{recipient_id}/vital-signs",
        headers=_headers(user_id),
        json=payload,
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
