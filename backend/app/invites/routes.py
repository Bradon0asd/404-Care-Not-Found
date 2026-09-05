from app.auth.current_user import get_current_user
from app.invites import invite_bp
from app.invites.schemas import (
    InviteEntrySchema,
    InviteProfileCreateSchema,
    InviteSchema,
)
from app.invites.service import (
    build_invite_url,
    complete_profile,
    create_invite,
    enter_invite,
    needs_profile,
)
from app.shared.response import api_success


@invite_bp.post("/invites")
@invite_bp.doc(summary="Create or return the owner's invite link", security=[{"UserIdHeader": []}])
def create_invite_api():
    invite = create_invite(owner=get_current_user())
    return api_success(_dump_invite(invite), status_code=201)


@invite_bp.post("/invites/<string:code>/enter")
@invite_bp.doc(summary="Open an invite link as the caregiver it belongs to")
def enter_invite_api(code):
    nurse = enter_invite(code=code)
    return api_success(_dump_entry(nurse))


@invite_bp.post("/invites/<string:code>/profile")
@invite_bp.arguments(InviteProfileCreateSchema, location="json")
@invite_bp.doc(summary="Save the caregiver's details on first visit")
def complete_profile_api(args, code):
    nurse = complete_profile(code=code, **args)
    return api_success(_dump_entry(nurse))


def _dump_invite(invite):
    payload = InviteSchema().dump(invite)
    payload["invite_url"] = build_invite_url(invite)
    return payload


def _dump_entry(nurse):
    payload = InviteEntrySchema().dump(nurse)
    payload["needs_profile"] = needs_profile(nurse)
    return payload
