from sqlalchemy import or_

from app.extensions import db
from app.models import CareRecipient, UserRole
from app.shared.errors import CareRecipientOwnerRequiredError
from app.shared.permissions import get_accessible_care_recipient


def create_recipient(*, current_user, name):
    """Owner and nurse ids come from the existing pairing, never from the client."""
    owner_id, nurse_id = _resolve_pair(current_user)
    recipient = CareRecipient(name=name, owner_id=owner_id, nurse_id=nurse_id)
    db.session.add(recipient)
    db.session.commit()
    return recipient


def list_recipients(*, current_user):
    return (
        CareRecipient.query.filter(
            or_(
                CareRecipient.owner_id == current_user.id,
                CareRecipient.nurse_id == current_user.id,
            )
        )
        .order_by(CareRecipient.id.asc())
        .all()
    )


def get_recipient(*, current_user, recipient_id):
    return get_accessible_care_recipient(
        current_user=current_user,
        recipient_id=recipient_id,
    )


def update_recipient(*, current_user, recipient_id, **changes):
    recipient = get_accessible_care_recipient(
        current_user=current_user,
        recipient_id=recipient_id,
    )
    if "name" in changes:
        recipient.name = changes["name"]
    db.session.commit()
    return recipient


def _resolve_pair(current_user):
    if current_user.role == UserRole.OWNER.value:
        return current_user.id, current_user.pair_user_id

    # A nurse cannot own a care recipient, so the paired owner has to exist first.
    if current_user.pair_user_id is None:
        raise CareRecipientOwnerRequiredError(
            "A nurse must be paired with an owner before creating a care recipient"
        )
    return current_user.pair_user_id, current_user.id
