from datetime import datetime

from SSHLogEntry import SSHLogEntry, SSHErrorInfo, SSHOtherInfo, SSHInvalidPassword, SSHAcceptedPassword
from utils import *


class SSHLogJournal:
    _log_entries: list[SSHLogEntry]

    def __init__(self):
        self._log_entries = []

    def __len__(self):  # return the number of log entries
        return len(self._log_entries)

    def __iter__(self): # return an iterator for log entries
        return iter(self._log_entries)

    def __contains__(self, item):   # check if the log entry is in the journal
        return item in self._log_entries

    def __getitem__(self, item):
        # if item is a slice object, return the corresponding slice of _log_entries
        if isinstance(item, slice):
            return self._log_entries[item]

        # if item is an integer, return the element at the specified index from _log_entries
        elif isinstance(item, int):
            return self._log_entries[item]

        # if item is a string, get ipv4 addresses from the logs
        elif isinstance(item, str):
            return self.get_logs_by_ipv4(item)

        # if item is a tuple of length 2 and both elements are datetime objects,
        # extract start_date and end_date from the tuple and return logs between these dates
        elif isinstance(item, tuple) and len(item) == 2 and all(isinstance(date, datetime) for date in item):
            start_date, end_date = item
            return self.get_logs_between_date(start_date, end_date)

        # if item does not match any supported type, raise a TypeError
        else:
            raise TypeError("Unsupported key type")

    def append(self, log_line: str):
        if re.match(r'failed password', log_line, re.IGNORECASE):
            ssh_log_type = SSHInvalidPassword(log_line)
        elif re.match(r'accepted password', log_line, re.IGNORECASE):
            ssh_log_type = SSHAcceptedPassword(log_line)
        elif re.match(r'error', log_line, re.IGNORECASE):
            ssh_log_type = SSHErrorInfo(log_line)
        else:
            ssh_log_type = SSHOtherInfo(log_line)

        if not ssh_log_type.validate():
            raise ValueError(f"Wrong data: {log_line}")

        self._log_entries.append(ssh_log_type)

    def get_logs_by_ipv4(self, ipv4) -> list[SSHLogEntry]:
        return [log for log in self._log_entries if str(log.ipv4()) == ipv4]

    def get_logs_between_date(self, start_date, end_date) -> list[SSHLogEntry]:
        return [log for log in self._log_entries if start_date <= log.timestamp <= end_date]

    def get_logs_by_type(self, message_type: MessageType):
        return [log for log in self._log_entries if get_msg_type(log.event_description) == message_type]
