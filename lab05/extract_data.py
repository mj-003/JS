import re
from collections import namedtuple
from typing import Tuple

# Regular expression pattern for extracting the data
log_pattern = re.compile(r"(?P<timestamp>\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s(?P<hostname>\w+)\s("
                         r"?P<app_component>\w+)\[(?P<pid>\d+)]:\s(?P<event_description>.+)")

LogEntry = namedtuple('LogEntry', ['timestamp', 'hostname', 'app_component', 'pid', 'event_description'])


def extract_data(log: str) -> LogEntry:
    """
    Extracts the timestamp, hostname, application component, PID, and event description from a log entry.

    :param log: A single log entry.
    :return: A tuple containing the timestamp, hostname, application component, PID, and event description.
    """
    match = log_pattern.match(log)
    if match:
        timestamp = match.group("timestamp")
        hostname = match.group("hostname")
        app_component = match.group("app_component")
        pid = int(match.group("pid"))
        event_description = match.group("event_description")
        return LogEntry(timestamp, hostname, app_component, pid, event_description)
    else:
        raise ValueError("Invalid log entry format")
