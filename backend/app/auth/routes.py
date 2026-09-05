import logging

from flask import redirect, request

from app.auth import auth_bp
from app.auth import service as auth_service
from app.auth.schemas import (
    LineLoginStartResponseSchema,
    LineLoginStartSchema,
    LoginSchema,
    SessionSchema,
)
from app.shared.errors import AppError
from app.shared.response import api_success

logger = logging.getLogger(__name__)


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


@auth_bp.post("/line/start")
@auth_bp.arguments(LineLoginStartSchema, location="json")
@auth_bp.doc(summary="Start LINE Login for the selected role")
def start_line_login(args):
    authorization_url = auth_service.start_line_login(role=args["role"])
    return api_success(
        LineLoginStartResponseSchema().dump({"authorization_url": authorization_url})
    )


@auth_bp.get("/line/callback")
@auth_bp.doc(summary="Handle the LINE Login redirect and open a session")
def line_login_callback():
    # LINE sends the user's browser here, so every outcome ends as a redirect the
    # frontend can read; the error code travels in the query string.
    declined = request.args.get("error")
    if declined:
        logger.info("line login declined at LINE: %s", declined)
        return redirect(_login_failure_url("LINE_LOGIN_DECLINED"))

    try:
        user = auth_service.complete_line_login(
            code=request.args.get("code"),
            state=request.args.get("state"),
        )
    except AppError as error:
        logger.info("line login failed: %s", error.code)
        return redirect(_login_failure_url(error.code))
    except Exception:
        logger.exception("line login callback crashed")
        return redirect(_login_failure_url("LINE_LOGIN_FAILED"))

    return redirect(
        auth_service.frontend_redirect_url(
            path_config_key="LINE_LOGIN_SUCCESS_PATH",
            default_path="/auth/callback",
            params={"login": "success", "role": user.role},
        )
    )


def _login_failure_url(code):
    return auth_service.frontend_redirect_url(
        path_config_key="LINE_LOGIN_FAILURE_PATH",
        default_path="/auth/role",
        params={"error": code},
    )
