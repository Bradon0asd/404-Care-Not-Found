class AppError(Exception):
    status_code = 400
    code = "APP_ERROR"

    def __init__(self, message):
        super().__init__(message)
        self.message = message


class UserNotFoundError(AppError):
    status_code = 404
    code = "USER_NOT_FOUND"


class UserAlreadyExistsError(AppError):
    status_code = 409
    code = "USER_ALREADY_EXISTS"


class UserPairingError(AppError):
    status_code = 400
    code = "USER_PAIRING_ERROR"


class LineConfigurationError(AppError):
    status_code = 503
    code = "LINE_NOT_CONFIGURED"


class InvalidLineSignatureError(AppError):
    status_code = 400
    code = "INVALID_LINE_SIGNATURE"
