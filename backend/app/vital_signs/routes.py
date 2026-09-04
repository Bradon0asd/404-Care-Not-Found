from app.auth.current_user import get_current_user
from app.shared.response import api_success
from app.vital_signs import dashboard_service
from app.vital_signs import service as vital_sign_service
from app.vital_signs import vital_sign_bp
from app.vital_signs.schemas import (
    DashboardSchema,
    VitalSignCreateSchema,
    VitalSignListQuerySchema,
    VitalSignSchema,
)


@vital_sign_bp.post("/care-recipients/<int:recipient_id>/vital-signs")
@vital_sign_bp.arguments(VitalSignCreateSchema, location="json")
@vital_sign_bp.doc(summary="Create a vital sign log", security=[{"UserIdHeader": []}])
def create_vital_sign(args, recipient_id):
    log = vital_sign_service.create_vital_sign(
        current_user=get_current_user(),
        recipient_id=recipient_id,
        **args,
    )
    return api_success(VitalSignSchema().dump(log), status_code=201)


@vital_sign_bp.get("/care-recipients/<int:recipient_id>/vital-signs")
@vital_sign_bp.arguments(VitalSignListQuerySchema, location="query")
@vital_sign_bp.doc(summary="List vital sign logs", security=[{"UserIdHeader": []}])
def list_vital_signs(args, recipient_id):
    logs = vital_sign_service.list_vital_signs(
        current_user=get_current_user(),
        recipient_id=recipient_id,
        **args,
    )
    return api_success(VitalSignSchema(many=True).dump(logs))


@vital_sign_bp.get("/care-recipients/<int:recipient_id>/dashboard")
@vital_sign_bp.doc(summary="Get the care log dashboard", security=[{"UserIdHeader": []}])
def get_dashboard(recipient_id):
    dashboard = dashboard_service.build_dashboard(
        current_user=get_current_user(),
        recipient_id=recipient_id,
    )
    return api_success(DashboardSchema().dump(dashboard))
