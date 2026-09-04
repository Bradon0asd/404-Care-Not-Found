from app.auth.current_user import get_current_user
from app.care_recipients import care_recipient_bp
from app.care_recipients import service as care_recipient_service
from app.care_recipients.schemas import (
    CareRecipientCreateSchema,
    CareRecipientSchema,
    CareRecipientUpdateSchema,
)
from app.shared.response import api_success


@care_recipient_bp.post("/care-recipients")
@care_recipient_bp.arguments(CareRecipientCreateSchema, location="json")
@care_recipient_bp.doc(summary="Create a care recipient", security=[{"UserIdHeader": []}])
def create_recipient(args):
    recipient = care_recipient_service.create_recipient(
        current_user=get_current_user(),
        **args,
    )
    return api_success(CareRecipientSchema().dump(recipient), status_code=201)


@care_recipient_bp.get("/care-recipients")
@care_recipient_bp.doc(summary="List accessible care recipients", security=[{"UserIdHeader": []}])
def list_recipients():
    recipients = care_recipient_service.list_recipients(current_user=get_current_user())
    return api_success(CareRecipientSchema(many=True).dump(recipients))


@care_recipient_bp.get("/care-recipients/<int:recipient_id>")
@care_recipient_bp.doc(summary="Get a care recipient", security=[{"UserIdHeader": []}])
def get_recipient(recipient_id):
    recipient = care_recipient_service.get_recipient(
        current_user=get_current_user(),
        recipient_id=recipient_id,
    )
    return api_success(CareRecipientSchema().dump(recipient))


@care_recipient_bp.patch("/care-recipients/<int:recipient_id>")
@care_recipient_bp.arguments(CareRecipientUpdateSchema, location="json")
@care_recipient_bp.doc(summary="Update a care recipient", security=[{"UserIdHeader": []}])
def update_recipient(args, recipient_id):
    recipient = care_recipient_service.update_recipient(
        current_user=get_current_user(),
        recipient_id=recipient_id,
        **args,
    )
    return api_success(CareRecipientSchema().dump(recipient))
