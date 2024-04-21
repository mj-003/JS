import re
from typing import List

from extract_data import LogEntry

# Regular expression patterns for extracting the data
user_pattern = re.compile(r"(invalid user |Invalid user |Failed password for invalid user |Failed password for "
                          r"|Accepted password for |session opened for user |session closed for user "
                          r"|user=)(?P<username>\w+)")
ipv4_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")


def get_user_from_log(entry: LogEntry) -> str | None:
    """
    Extracts the username from a log entry.

    :param entry:
    :return: The username.
    """

    match = user_pattern.search(entry.event_description)
    return match.group("username") if match else None


def get_ipv4_from_log(entry: LogEntry) -> List[str]:
    """
    Extracts the IPv4 addresses from a log entry.

    :param entry:
    :return: A list of IPv4 addresses.
    """
    return ipv4_pattern.findall(entry.event_description)


