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


class AuthenticationError(AppError):
    status_code = 401
    code = "AUTHENTICATION_REQUIRED"


class PermissionDeniedError(AppError):
    status_code = 403
    code = "PERMISSION_DENIED"


class DiaryNotFoundError(AppError):
    status_code = 404
    code = "DIARY_NOT_FOUND"


class StickyNoteNotFoundError(AppError):
    status_code = 404
    code = "STICKY_NOTE_NOT_FOUND"


class CareRecipientNotFoundError(AppError):
    status_code = 404
    code = "CARE_RECIPIENT_NOT_FOUND"


class CareRecipientOwnerRequiredError(AppError):
    status_code = 400
    code = "CARE_RECIPIENT_OWNER_REQUIRED"


class CareScheduleNotFoundError(AppError):
    status_code = 404
    code = "CARE_SCHEDULE_NOT_FOUND"


class LineConfigurationError(AppError):
    status_code = 503
    code = "LINE_NOT_CONFIGURED"


class InvalidLineSignatureError(AppError):
    status_code = 400
    code = "INVALID_LINE_SIGNATURE"


class LineRecipientNotPairedError(AppError):
    status_code = 400
    code = "LINE_RECIPIENT_NOT_PAIRED"


class InvalidUploadError(AppError):
    status_code = 400
    code = "INVALID_UPLOAD"


class GoogleAiConfigurationError(AppError):
    status_code = 503
    code = "GOOGLE_AI_NOT_CONFIGURED"


class GoogleAiApiError(AppError):
    status_code = 502
    code = "GOOGLE_AI_API_ERROR"


class InviteNotFoundError(AppError):
    status_code = 404
    code = "INVITE_NOT_FOUND"


class InviteRevokedError(AppError):
    status_code = 410
    code = "INVITE_REVOKED"
