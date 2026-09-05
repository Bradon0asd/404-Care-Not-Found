from app.auth import auth_bp
from app.auth import service as auth_service
from app.auth.schemas import LoginSchema, SessionSchema
from app.shared.response import api_success


@auth_bp.post("/login")
@auth_bp.arguments(LoginSchema, location="json")
@auth_bp.doc(summary="Start a session for a LINE id")
def login(args):
    user = auth_service.login(**args)
    return api_success(SessionSchema().dump(user))


@auth_bp.post("/logout")
@auth_bp.doc(summary="End the current session")
def logout():
    auth_service.logout()
    return api_success()


@auth_bp.get("/session")
@auth_bp.doc(summary="Read the current session user")
def read_session():
    user = auth_service.require_session_user()
    return api_success(SessionSchema().dump(user))
