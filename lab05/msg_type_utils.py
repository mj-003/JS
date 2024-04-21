import logging
from enum import Enum

from get_from_log import get_user_from_log


class MessageType(Enum):
    SUCCESSFUL_LOGIN = "successful login"
    FAILED_LOGIN = "failed login"
    CONNECTION_CLOSED = "connection closed"
    INVALID_PASSWORD = "invalid password"
    INVALID_USERNAME = "invalid username"
    BREAK_IN_ATTEMPT = "break-in attempt"
    OTHER = "other"


def get_msg_type(entry) -> MessageType:
    if "Accepted password for" or "Accepted publickey for" in entry.event_description:
        return MessageType.SUCCESSFUL_LOGIN
    elif "Failed password for" or "Failed publickey for" in entry.event_description:
        if "invalid user" in entry.event_description:
            return MessageType.INVALID_USERNAME
        elif "invalid password" in entry.event_description:
            return MessageType.INVALID_PASSWORD
        else:
            return MessageType.FAILED_LOGIN
    elif "Connection closed" in entry.event_description:
        return MessageType.CONNECTION_CLOSED
    elif "Invalid user" in entry.event_description:
        return MessageType.INVALID_USERNAME
    elif "BREAK-IN" in entry.event_description:
        return MessageType.BREAK_IN_ATTEMPT
    else:
        return MessageType.OTHER


def analyze_msg_type(entry, logger: logging.Logger):
    msg_type = get_msg_type(entry)

    if msg_type == MessageType.SUCCESSFUL_LOGIN:
        logger.info(
            f"Hostname: {entry.hostname}, Username: {get_user_from_log(entry.event_description)}, message: {entry.event_description}")
    elif msg_type == MessageType.FAILED_LOGIN:
        logger.warning(
            f"Hostname: {entry.hostname}, Username: {get_user_from_log(entry.event_description)}, message: {entry.event_description}")
    elif msg_type == MessageType.CONNECTION_CLOSED:
        logger.debug(f"Hostname: {entry.hostname}, message: {entry.event_description}")
    elif msg_type == MessageType.INVALID_PASSWORD:
        logger.error(f"Hostname: {entry.hostname}, message: {entry.event_description}")
    elif msg_type == MessageType.INVALID_USERNAME:
        logger.error(f"Hostname: {entry.hostname}, message: {entry.event_description}")
    elif msg_type == MessageType.BREAK_IN_ATTEMPT:
        logger.critical(f"Hostname: {entry.hostname}, message: {entry.event_description}")
    else:
        logger.debug(f"Hostname: {entry.hostname}, message: {entry.event_description}")
