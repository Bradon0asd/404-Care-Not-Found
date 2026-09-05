from flask import g

from app.auth.decorators import login_required
from app.shared.response import api_success
from app.diaries import diary_bp
from app.diaries.service import (
    create_diary,
    list_diaries,
    get_diary,
    update_diary,
    delete_diary,
)
from app.diaries.schemas import DiaryCreateSchema, DiarySchema, DiaryUpdateSchema


@diary_bp.post("/diaries")
@login_required
@diary_bp.arguments(DiaryCreateSchema, location="json")
@diary_bp.doc(summary="Create a diary", security=[{"UserIdHeader": []}])
def create_diary_api(args):
    diary = create_diary(current_user=g.current_user, **args)
    return api_success(DiarySchema().dump(diary), status_code=201)


@diary_bp.get("/diaries")
@diary_bp.doc(summary="List diaries", security=[{"UserIdHeader": []}])
@login_required
def list_diaries_api():
    diaries = list_diaries(current_user=g.current_user)
    return api_success(DiarySchema(many=True).dump(diaries))


@diary_bp.get("/diaries/<int:diary_id>")
@diary_bp.doc(summary="Get a diary", security=[{"UserIdHeader": []}])
@login_required
def get_diary_api(diary_id):
    diary = get_diary(current_user=g.current_user, diary_id=diary_id)
    return api_success(DiarySchema().dump(diary))


@diary_bp.patch("/diaries/<int:diary_id>")
@login_required
@diary_bp.arguments(DiaryUpdateSchema, location="json")
@diary_bp.doc(summary="Update a diary", security=[{"UserIdHeader": []}])
def update_diary_api(args, diary_id):
    diary = update_diary(
        current_user=g.current_user,
        diary_id=diary_id,
        **args,
    )
    return api_success(DiarySchema().dump(diary))


@diary_bp.delete("/diaries/<int:diary_id>")
@diary_bp.doc(summary="Delete a diary", security=[{"UserIdHeader": []}])
@login_required
def delete_diary_api(diary_id):
    delete_diary(current_user=g.current_user, diary_id=diary_id)
    return api_success()
