import re
import sys
from datetime import datetime

from sort_logs import *
from dictionaries import *
from filters import *


def read_log():
    pattern = r'^(\S+) - - \[([\w:/]+ [+\-]\d{4})\] "(.*?)" (\d{3}) (\d+|-)$'
    date_pattern = "%d/%b/%Y:%H:%M:%S %z"
    entries = []
    for entry in sys.stdin:
        match = re.match(pattern, entry)
        if match:
            host_name, date_time, request, code, bytes = match.groups()
            date_time_obj = datetime.strptime(date_time, date_pattern)
            bytes = int(bytes) if bytes != "-" else None
            entries.append((host_name, date_time_obj, request, int(code), bytes))
        else:
            print(f"Line: {entry} doesn't match the pattern.")
    return entries


if __name__ == "__main__":
    log_entries = read_log()
    log_dict = log_to_dict(log_entries)
    # print_dict_entry_dates(log_dict)
    addrs = get_addrs(log_dict)
    print(addrs)








