def is_active_member_status(status: str) -> bool:
    return status in {"member", "administrator", "creator", "owner"}


def is_blocked_bot_error(error: Exception) -> bool:
    message = str(error).lower()
    return "bot was blocked by the user" in message
