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

