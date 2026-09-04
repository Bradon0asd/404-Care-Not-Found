from app.auth.current_user import get_current_user
from app.shared.response import api_success
from app.diaries import diary_bp
from app.diaries import service as diary_service
from app.diaries.schemas import DiaryCreateSchema, DiarySchema, DiaryUpdateSchema


@diary_bp.post("/diaries")
@diary_bp.arguments(DiaryCreateSchema, location="json")
@diary_bp.doc(summary="Create a diary", security=[{"UserIdHeader": []}])
def create_diary(args):
    diary = diary_service.create_diary(current_user=get_current_user(), **args)
    return api_success(DiarySchema().dump(diary), status_code=201)


@diary_bp.get("/diaries")
@diary_bp.doc(summary="List diaries", security=[{"UserIdHeader": []}])
def list_diaries():
    diaries = diary_service.list_diaries(current_user=get_current_user())
    return api_success(DiarySchema(many=True).dump(diaries))


@diary_bp.get("/diaries/<int:diary_id>")
@diary_bp.doc(summary="Get a diary", security=[{"UserIdHeader": []}])
def get_diary(diary_id):
    diary = diary_service.get_diary(current_user=get_current_user(), diary_id=diary_id)
    return api_success(DiarySchema().dump(diary))


@diary_bp.patch("/diaries/<int:diary_id>")
@diary_bp.arguments(DiaryUpdateSchema, location="json")
@diary_bp.doc(summary="Update a diary", security=[{"UserIdHeader": []}])
def update_diary(args, diary_id):
    diary = diary_service.update_diary(
        current_user=get_current_user(),
        diary_id=diary_id,
        **args,
    )
    return api_success(DiarySchema().dump(diary))


@diary_bp.delete("/diaries/<int:diary_id>")
@diary_bp.doc(summary="Delete a diary", security=[{"UserIdHeader": []}])
def delete_diary(diary_id):
    diary_service.delete_diary(current_user=get_current_user(), diary_id=diary_id)
    return api_success()
