from app.users import user_bp
from app.shared.response import api_success
from app.users import service as user_service
from app.users.schemas import UserCreateSchema, UserPairSchema, UserSchema


@user_bp.post("/users")
@user_bp.arguments(UserCreateSchema, location="json")
@user_bp.doc(summary="Create a user")
def create_user(args):
    user = user_service.create_user(**args)
    return api_success(UserSchema().dump(user), status_code=201)


@user_bp.get("/users/<int:user_id>")
@user_bp.doc(summary="Get a user")
def get_user(user_id):
    user = user_service.get_user(user_id=user_id)
    return api_success(UserSchema().dump(user))


@user_bp.post("/users/<int:user_id>/pair")
@user_bp.arguments(UserPairSchema, location="json")
@user_bp.doc(summary="Pair a user with another user")
def pair_user(args, user_id):
    user = user_service.get_user(user_id=user_id)
    target_user = user_service.get_user(user_id=args["pair_user_id"])
    user_service.pair_users(user, target_user)
    return api_success(UserSchema().dump(user))


@user_bp.delete("/users/<int:user_id>/pair")
@user_bp.doc(summary="Remove a user's pairing")
def unpair_user(user_id):
    user = user_service.get_user(user_id=user_id)
    user_service.unpair_users(user)
    return api_success(UserSchema().dump(user))
