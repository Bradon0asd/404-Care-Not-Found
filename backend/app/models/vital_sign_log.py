from enum import StrEnum

from app.extensions import db
from app.models.diary import utc_now


class VitalSignType(StrEnum):
    BLOOD_PRESSURE = "blood_pressure"
    BLOOD_GLUCOSE = "blood_glucose"
    HEART_RATE = "heart_rate"
    OXYGEN_SATURATION = "oxygen_saturation"
    TEMPERATURE = "temperature"
    RESPIRATORY_RATE = "respiratory_rate"


# Units are decided by the server, never by the client.
VITAL_SIGN_UNITS = {
    VitalSignType.BLOOD_PRESSURE.value: "mmHg",
    VitalSignType.BLOOD_GLUCOSE.value: "mg/dL",
    VitalSignType.HEART_RATE.value: "bpm",
    VitalSignType.OXYGEN_SATURATION.value: "%",
    VitalSignType.TEMPERATURE.value: "\u00b0C",
    VitalSignType.RESPIRATORY_RATE.value: "breaths/min",
}


class VitalSignLog(db.Model):
    __tablename__ = "vital_sign_logs"

    id = db.Column(db.Integer, primary_key=True)
    care_recipient_id = db.Column(
        db.Integer,
        db.ForeignKey("care_recipients.id"),
        nullable=False,
        index=True,
    )
    creator_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )
    vital_type = db.Column(db.String(30), nullable=False, index=True)
    value = db.Column(db.Float, nullable=False)
    secondary_value = db.Column(db.Float, nullable=True)
    unit = db.Column(db.String(20), nullable=False)
    measured_at = db.Column(db.DateTime, nullable=False, index=True)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
        server_default=db.func.current_timestamp(),
    )

    care_recipient = db.relationship("CareRecipient", back_populates="vital_sign_logs")
    creator = db.relationship("User", back_populates="created_vital_sign_logs")
