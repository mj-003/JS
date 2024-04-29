import re
from enum import Enum


class MessageType(Enum):
    INVALID_PASSWORD = "invalid password"
    ACCEPTED_PASSWORD = "accepted password"
    OTHER = "other"
    ERROR = "error"


# Determines the message type of log entry
def get_msg_type(event_description: str) -> MessageType:
    if re.match(r'failed password', event_description, re.IGNORECASE):
        return MessageType.INVALID_PASSWORD
    elif re.match(r'accepted password', event_description, re.IGNORECASE):
        return MessageType.ACCEPTED_PASSWORD
    elif re.match(r'error', event_description, re.IGNORECASE):
        return MessageType.ERROR
    else:
        return MessageType.OTHER




