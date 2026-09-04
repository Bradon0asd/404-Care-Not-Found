from app.extensions import db
from app.models import CareRecipient, User, UserRole


def test_user_returns_recipients_for_its_role(app):
    with app.app_context():
        owner = User(line_id="owner-line-id", role=UserRole.OWNER.value)
        nurse = User(line_id="nurse-line-id", role=UserRole.NURSE.value)
        recipient = CareRecipient(name="Patient", owner=owner, nurse=nurse)
        db.session.add(recipient)
        db.session.commit()

        assert owner.care_recipients == [recipient]
        assert nurse.care_recipients == [recipient]
