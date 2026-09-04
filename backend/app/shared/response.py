def api_success(data=None, *, message=None, status_code=200, meta=None):
    payload = {"success": True, "data": data}
    if message is not None:
        payload["message"] = message
    if meta is not None:
        payload["meta"] = meta
    return payload, status_code


def api_error(*, code, message, status_code=400, details=None):
    error = {"code": code, "message": message}
    if details is not None:
        error["details"] = details
    return {"success": False, "error": error}, status_code
