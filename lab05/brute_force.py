import re
from collections import defaultdict

from get_from_log import get_user_from_log, get_ipv4_from_log


def detect_bruteforce(logs, max_interval=100, max_attempts=60, single_user=False):
    if max_interval < 0 or max_attempts < 0:
        print("Parameters must be positive integers.")
        return

    failed_password_pattern = r'Failed password for (\S+).*'
    repeat_pattern = r'message repeated (\S+) times:'
    ip_attempts = defaultdict(list)

    for log in logs:
        user = get_user_from_log(log)

        if user is None:
            user = re.search(failed_password_pattern, log[-1]).group(1) if re.search(failed_password_pattern,
                                                                                     log[-1]) else None

        if re.search(failed_password_pattern, log[-1]):
            ip = get_ipv4_from_log(log)[0]
            key = ip[-1] if not single_user else str(ip[-1] + " " + user)
            ip_attempts[key].append(log[0])

            if re.search(repeat_pattern, log[-1]):
                times = re.search(repeat_pattern, log[-1]).group(1)
                for _ in range(int(times) - 1):
                    ip_attempts[key].append(log[0])

            if len(ip_attempts[key]) >= max_attempts:
                time_diff = (ip_attempts[key][-1] - ip_attempts[key][0]).total_seconds()

                if time_diff <= max_interval:
                    if not single_user:
                        print(
                            f"Bruteforce attack attempt detected from IP address {ip}, start of attack: {ip_attempts[key][0]}, end of attack: {ip_attempts[key][-1]}")
                    else:
                        print(
                            f"Bruteforce attack attempt detected from IP address {ip} and user {user}, start of attack: {ip_attempts[key][0]}, end of attack: {ip_attempts[key][-1]}")
                    ip_attempts[key] = []
                else:
                    ip_attempts[key] = ip_attempts[key][1:]
