import re
from abc import ABC, abstractmethod
from ipaddress import IPv4Address

from utils import MessageType, get_msg_type


class SSHLogEntry(ABC):
    timestamp: str
    hostname: str | None
    app_component: str
    pid: int
    event_description: str
    _original_log: str

    _log_pattern = re.compile(r"(?P<timestamp>\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})\s(?P<hostname>\w+)\s("
                              r"?P<app_component>\w+)\[(?P<pid>\d+)]:\s(?P<event_description>.+)")

    _user_pattern = re.compile(r"(invalid user |Invalid user |Failed password for invalid user |Failed password for "
                               r"|Accepted password for |session opened for user |session closed for user "
                               r"|user=)(?P<username>\w+)")

    _ipv4_pattern = re.compile(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b")

    def __init__(self, log_line: str):  # extract the data from the log entry and initialize the class attributes
        match = self._log_pattern.match(log_line)
        if match:
            self.timestamp = match.group("timestamp")
            self.hostname = match.group("hostname")
            self.app_component = match.group("app_component")
            self.pid = int(match.group("pid"))
            self.event_description = match.group("event_description")
            self._original_log = log_line.strip()
        else:
            print(f"Invalid log entry format: {log_line}")

    def __str__(self) -> str:  # return string of log
        user = self.hostname
        if user is None or user == 'unknown':
            user = "Unknown user"
        return f"{user} - {self.timestamp} {self.app_component}[{self.pid}]: {self.event_description}"

    def __repr__(self) -> str:  # return the class name and the original log entry
        return (
            f"<{self.__class__.__name__}("
            f"timestamp='{self.timestamp}', "
            f"hostname='{self.hostname}', "
            f"app_component='{self.app_component}', "
            f"pid={self.pid}, "
            f"event_description='{self.event_description}'"
            f")>"
        )

    def __eq__(self, other) -> bool:  # compare the log entries
        if not isinstance(other, SSHLogEntry):
            return False
        return (
                (self.timestamp, self.hostname, self.app_component, self.pid, self.event_description) ==
                (other.timestamp, other.hostname, other.app_component, other.pid, other.event_description)
        )

    def __lt__(self, other):  # compare the timestamps of the log entries
        if not isinstance(other, SSHLogEntry):
            raise TypeError(f"'<' not supported between instances of '{self.__class__.__name__}' and '{type(other)}'")
        return self.timestamp < other.timestamp

    def __gt__(self, other):  # compare the timestamps of the log entries
        if not isinstance(other, SSHLogEntry):
            raise TypeError(f"'>' not supported between instances of '{self.__class__.__name__}' and '{type(other)}'")
        return self.timestamp > other.timestamp

    def ipv4(self) -> IPv4Address:  # extract the IPv4 address from the log entry
        addresses = self._ipv4_pattern.findall(self.event_description)
        return IPv4Address(addresses[0]) if addresses else None

    @abstractmethod
    def validate(self) -> bool:  # abstract method to validate the log entry
        pass

    #
    @property
    def has_ip(self) -> bool:
        return bool(self.ipv4())


# inherited class for failed password
class SSHInvalidPassword(SSHLogEntry):
    def __init__(self, log_line: str):
        super().__init__(log_line)

    def validate(self) -> bool:
        match = self._user_pattern.search(self._original_log)
        return (
                get_msg_type(self.event_description) == MessageType.INVALID_PASSWORD
                and self.timestamp == match.group("timestamp")
                and self.hostname == match.group("hostname")
                and self.app_component == match.group("app_component")
                and self.pid == int(match.group("pid"))
                and self.event_description == match.group("event_description")
        )


# inherited class for successful login
class SSHAcceptedPassword(SSHLogEntry):
    def __init__(self, log_line: str):
        super().__init__(log_line)

    def validate(self) -> bool:
        match = self._user_pattern.search(self._original_log)
        return (
                get_msg_type(self.event_description) == MessageType.ACCEPTED_PASSWORD
                and self.timestamp == match.group("timestamp")
                and self.hostname == match.group("hostname")
                and self.app_component == match.group("app_component")
                and self.pid == int(match.group("pid"))
                and self.event_description == match.group("event_description")
        )


# inherited class for error information
class SSHErrorInfo(SSHLogEntry):
    def __init__(self, log_line: str):
        super().__init__(log_line)

    def validate(self) -> bool:
        match = self._user_pattern.search(self._original_log)
        return (
                get_msg_type(self.event_description) == MessageType.ERROR
                and self.timestamp == match.group("timestamp")
                and self.hostname == match.group("hostname")
                and self.app_component == match.group("app_component")
                and self.pid == int(match.group("pid"))
                and self.event_description == match.group("event_description")
        )


# inherited class for other information
class SSHOtherInfo(SSHLogEntry):
    def __init__(self, log_line: str):
        super().__init__(log_line)

    def validate(self) -> bool:
        super().validate()
        return True
