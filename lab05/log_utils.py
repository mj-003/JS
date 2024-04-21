import re
from collections import namedtuple
from typing import List

# Regular expression pattern for extracting the data
log_pattern = re.compile(r"(?P<timestamp>\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s(?P<hostname>\w+)\s("
                         r"?P<app_component>\w+)\[(?P<pid>\d+)]:\s(?P<event_description>.+)")


# Regular expression patterns for extracting the data
user_pattern = re.compile(r"(invalid user |Invalid user |Failed password for invalid user |Failed password for "
                          r"|Accepted password for |session opened for user |session closed for user "
                          r"|user=)(?P<username>\w+)")
ipv4_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")


# Named tuple for storing the log entry data
LogEntry = namedtuple('LogEntry', ['timestamp', 'hostname', 'app_component', 'pid', 'event_description'])


# Extracts the timestamp, hostname, application component, PID, and event description from a log entry
def extract_data(log: str) -> LogEntry:
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


# Extracts the username from a log entry
def get_user_from_log(entry: LogEntry) -> str | None:
    match = user_pattern.search(entry.event_description)
    return match.group("username") if match else None


# Extracts the IPv4 addresses from a log entry
def get_ipv4_from_log(entry: LogEntry) -> List[str]:
    return ipv4_pattern.findall(entry.event_description)




