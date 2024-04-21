import logging
import re
from enum import Enum
from get_from_log import get_user_from_log


class MessageType(Enum):
    SUCCESSFUL_LOGIN = "successful login"
    FAILED_LOGIN = "failed login"
    CONNECTION_CLOSED = "connection closed"
    CONNECTION_OPENED = "connection opened"
    INVALID_PASSWORD = "invalid password"
    INVALID_USERNAME = "invalid username"
    BREAK_IN_ATTEMPT = "break-in attempt"
    OTHER = "other"


def get_msg_type(entry) -> MessageType:
    if re.match(r'Accepted (password|publickey) for', entry.event_description, re.IGNORECASE):
        return MessageType.SUCCESSFUL_LOGIN

    elif re.match(r'(Failed password|Failed publickey for)', entry.event_description, re.IGNORECASE):

        if "invalid user" in entry.event_description:
            return MessageType.INVALID_USERNAME
        elif "invalid password" in entry.event_description:
            return MessageType.INVALID_PASSWORD
        else:
            return MessageType.FAILED_LOGIN

    elif re.match(r'Connection closed', entry.event_description, re.IGNORECASE):
        return MessageType.CONNECTION_CLOSED

    elif re.match(r'Invalid user', entry.event_description, re.IGNORECASE):
        return MessageType.INVALID_USERNAME

    elif re.match(r'BREAK-IN', entry.event_description):
        return MessageType.BREAK_IN_ATTEMPT

    else:
        return MessageType.OTHER


def analyze_msg_type(entry, logger: logging.Logger):
    msg_type = get_msg_type(entry)

    if msg_type == MessageType.SUCCESSFUL_LOGIN:
        logger.info(
            f"Hostname: {entry.hostname}, Username: {get_user_from_log(entry)}, message: {entry.event_description}")

    elif msg_type == MessageType.FAILED_LOGIN:
        logger.warning(
            f"Hostname: {entry.hostname}, Username: {get_user_from_log(entry)}, message: {entry.event_description}")

    elif msg_type == MessageType.CONNECTION_CLOSED:
        logger.debug(f"Hostname: {entry.hostname}, Username: {get_user_from_log(entry)}, message: {entry.event_description}")

    elif msg_type == MessageType.INVALID_PASSWORD:
        logger.error(f"Hostname: {entry.hostname}, Username: {get_user_from_log(entry)}, message: {entry.event_description}")

    elif msg_type == MessageType.INVALID_USERNAME:
        logger.error(f"Hostname: {entry.hostname}, Username: {get_user_from_log(entry)}, message: {entry.event_description}")

    elif msg_type == MessageType.BREAK_IN_ATTEMPT:
        logger.critical(f"Hostname: {entry.hostname}, Username: {get_user_from_log(entry)}, message: {entry.event_description}")

    else:
        logger.debug(f"Hostname: {entry.hostname}, Username: {get_user_from_log(entry)}, message: {entry.event_description}")
