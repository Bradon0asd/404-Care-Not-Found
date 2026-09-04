from app.extensions import db
from app.models import CareRecipient
from app.shared.errors import CareRecipientNotFoundError, PermissionDeniedError


def get_accessible_care_recipient(*, current_user, recipient_id):
    """Return the care recipient only if the current user is its owner or nurse."""
    recipient = db.session.get(CareRecipient, recipient_id)
    if recipient is None:
        raise CareRecipientNotFoundError("Care recipient not found")
    require_care_recipient_access(recipient=recipient, current_user=current_user)
    return recipient


def require_care_recipient_access(*, recipient, current_user):
    if current_user.id not in (recipient.owner_id, recipient.nurse_id):
        raise PermissionDeniedError("Care recipient is not accessible to the current user")
    return recipient
