from app.api import api_bp
from app.api import service as user_service
from app.api.schemas import UserCreateSchema, UserSchema
from app.extensions import parser


@api_bp.get("/health")
def health():
    return {"status": "ok"}, 200


@api_bp.post("/users")
@parser.use_args(UserCreateSchema(), location="json")
def create_user(args):
    user = user_service.create_user(**args)
    return UserSchema().dump(user), 201


@api_bp.get("/users/<int:user_id>")
def get_user(user_id):
    user = user_service.get_user(user_id=user_id)
    return UserSchema().dump(user), 200
