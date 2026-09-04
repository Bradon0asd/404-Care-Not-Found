from app.users import user_bp
from app.common.response import api_success
from app.extensions import parser
from app.users import service as user_service
from app.users.schemas import UserCreateSchema, UserSchema


@user_bp.post("/users")
@parser.use_args(UserCreateSchema(), location="json")
def create_user(args):
    user = user_service.create_user(**args)
    return api_success(UserSchema().dump(user), status_code=201)


@user_bp.get("/users/<int:user_id>")
def get_user(user_id):
    user = user_service.get_user(user_id=user_id)
    return api_success(UserSchema().dump(user))
