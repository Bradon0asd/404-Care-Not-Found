from flask import g

from app.auth.decorators import login_required
from app.care_schedules import care_schedule_bp
from app.care_schedules import service as care_schedule_service
from app.care_schedules.schemas import (
    CareScheduleCreateSchema,
    CareScheduleListQuerySchema,
    CareScheduleSchema,
    CareScheduleUpdateSchema,
)
from app.shared.response import api_success


@care_schedule_bp.post("/care-recipients/<int:recipient_id>/schedules")
@login_required
@care_schedule_bp.arguments(CareScheduleCreateSchema, location="json")
@care_schedule_bp.doc(summary="Create a care schedule", security=[{"UserIdHeader": []}])
def create_schedule(args, recipient_id):
    schedule = care_schedule_service.create_schedule(
        current_user=g.current_user,
        recipient_id=recipient_id,
        **args,
    )
    return api_success(CareScheduleSchema().dump(schedule), status_code=201)


@care_schedule_bp.get("/care-recipients/<int:recipient_id>/schedules")
@login_required
@care_schedule_bp.arguments(CareScheduleListQuerySchema, location="query")
@care_schedule_bp.doc(summary="List care schedules", security=[{"UserIdHeader": []}])
def list_schedules(args, recipient_id):
    schedules = care_schedule_service.list_schedules(
        current_user=g.current_user,
        recipient_id=recipient_id,
        **args,
    )
    return api_success(CareScheduleSchema(many=True).dump(schedules))


@care_schedule_bp.get("/schedules/<int:schedule_id>")
@care_schedule_bp.doc(summary="Get a care schedule", security=[{"UserIdHeader": []}])
@login_required
def get_schedule(schedule_id):
    schedule = care_schedule_service.get_schedule(
        current_user=g.current_user,
        schedule_id=schedule_id,
    )
    return api_success(CareScheduleSchema().dump(schedule))


@care_schedule_bp.patch("/schedules/<int:schedule_id>")
@login_required
@care_schedule_bp.arguments(CareScheduleUpdateSchema, location="json")
@care_schedule_bp.doc(summary="Update a care schedule", security=[{"UserIdHeader": []}])
def update_schedule(args, schedule_id):
    schedule = care_schedule_service.update_schedule(
        current_user=g.current_user,
        schedule_id=schedule_id,
        **args,
    )
    return api_success(CareScheduleSchema().dump(schedule))


@care_schedule_bp.delete("/schedules/<int:schedule_id>")
@care_schedule_bp.doc(summary="Delete a care schedule", security=[{"UserIdHeader": []}])
@login_required
def delete_schedule(schedule_id):
    care_schedule_service.delete_schedule(
        current_user=g.current_user,
        schedule_id=schedule_id,
    )
    return api_success()
