import re
from collections import defaultdict
from datetime import datetime

from log_utils import get_user_from_log, get_ipv4_from_log


def detect_bruteforce(logs, max_interval=100, max_attempts=60, single_user=False):
    # Check if max_interval and max_attempts are positive integers
    if max_interval < 0 or max_attempts < 0:
        print("Parameters must be positive integers.")
        return

    # Regular expression patterns
    failed_password_pattern = r'Failed password for (\S+).*'
    repeat_pattern = r'message repeated (\d+) times:'

    # Dictionary to store IP attempts
    ip_attempts = defaultdict(list)

    # Iterate through logs
    for log in logs:
        user = get_user_from_log(log)

        # If user is not found, extract from log message
        if user is None:
            user_match = re.search(failed_password_pattern, log[-1])
            user = user_match.group(1) if user_match else None

        # Continue to next log if user is not found or log does not contain failed password attempt
        if not user or not re.search(failed_password_pattern, log[-1]):
            continue

        ip = get_ipv4_from_log(log)

        # Continue to next log if IP address is not found
        if not ip:
            continue

        # Define key for IP attempts dictionary
        ip_key = ip[-1] if not single_user else f"{ip[-1]} {user}"

        # Append log timestamp to IP attempts
        ip_attempts[ip_key].append(log[0])

        # Extend IP attempts if log contains repeat pattern
        if repeat_match := re.search(repeat_pattern, log[-1]):
            times = int(repeat_match.group(1))
            ip_attempts[ip_key].extend([log[0]] * (times - 1))

        # Check if number of attempts exceeds max_attempts
        if len(ip_attempts[ip_key]) >= max_attempts:
            start_time = datetime.strptime(ip_attempts[ip_key][0], "%b %d %H:%M:%S")
            end_time = datetime.strptime(ip_attempts[ip_key][-1], "%b %d %H:%M:%S")
            time_diff = (end_time - start_time).total_seconds()

            # If time difference is within max_interval, print detection message and reset IP attempts
            if time_diff <= max_interval:
                message = f"Brute force detected, IP: {ip[-1]}"
                if single_user:
                    message += f", user: {user}"
                message += f", start: {start_time}, end: {end_time}, attempts: {len(ip_attempts[ip_key])}"
                print(message)
                ip_attempts[ip_key] = []

            # Otherwise, remove the oldest attempt from IP attempts
            else:
                ip_attempts[ip_key] = ip_attempts[ip_key][1:]
