import re
from typing import List

# Regular expression patterns for extracting the data
user_pattern = re.compile(r"(invalid user |Invalid user |Failed password for invalid user |Failed password for "
                          r"|Accepted password for |user=)(?P<username>\w+)")
ipv4_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")


def get_user_from_log(event_description: str) -> str | None:
    """
    Extracts the username from a log entry.

    :param event_description: A single log entry.
    :return: The username.
    """
    match = user_pattern.search(event_description)
    return match.group("username") if match else None


def get_ipv4_from_log(event_description: str) -> List[str]:
    """
    Extracts the IPv4 addresses from a log entry.

    :param event_description: A single log entry.
    :return: A list of IPv4 addresses.
    """
    return ipv4_pattern.findall(event_description)


