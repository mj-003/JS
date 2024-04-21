import random
import datetime
from typing import List, Tuple, Iterable
import statistics
from log_utils import get_user_from_log, LogEntry
from msg_type_utils import get_msg_type, MessageType


# a) return n random log entries for a given user
def get_random_user_logs(logs: Iterable[LogEntry], n: int) -> List[LogEntry]:
    users_with_logs = list(filter(lambda log: get_user_from_log(log) is not None, logs))  # filter out logs without user
    user_name = get_user_from_log(random.choice(users_with_logs))

    user_logs = [log for log in logs if get_user_from_log(log) == user_name]  # get all logs for the user
    return random.sample(user_logs, min(n, len(user_logs)))  # return n random logs for the user


# b) calculate the average session duration and standard deviation for all users
#   I. for all users

def get_avg_duration_and_deviation(logs: Iterable[LogEntry]) -> Tuple[float, float]:
    session_starts: dict[int, str] = {}
    session_durations = []

    for log in logs:
        if "session opened" in log.event_description:
            session_starts[log.pid] = log.timestamp

        elif "session closed" in log.event_description and log.pid in session_starts:
            start_time = session_starts.pop(log.pid, None)  # remove the session start time
            if start_time:
                start_ = datetime.datetime.strptime(start_time, "%b %d %H:%M:%S")
                end_ = datetime.datetime.strptime(log.timestamp, "%b %d %H:%M:%S")
                duration = (end_ - start_).total_seconds()  # calculate the duration of the session
                session_durations.append(duration)

    if session_durations:  # if there are any sessions
        average_duration = statistics.mean(session_durations)
        std_deviation = (statistics.stdev(session_durations) if len(session_durations) > 1 else 0.0)
        return average_duration, std_deviation
    else:
        return 0.0, 0.0


# b) calculate the average session duration and standard deviation for all users
#   II. grouped by user
def get_stats_grouped_by_user(logs: Iterable[LogEntry]) -> dict[str, Tuple[float, float]]:
    user_stats: dict[str, tuple[float, float]] = {}

    users = set([get_user_from_log(log) for log in logs])  # get all unique users

    for user in users:
        user_logs = [log for log in logs if get_user_from_log(log) == user]  # get all logs for the user
        user_stats[user] = get_avg_duration_and_deviation(
            user_logs)  # calculate the average duration and standard deviation

    return user_stats


# c) Calculate the most and least frequent users
def get_most_and_least_frequent_users(logs: Iterable[LogEntry]):
    user_logins: dict[str, int] = {}

    for log in logs:
        user_name = get_user_from_log(log)
        if user_name and get_msg_type(log) == MessageType.SUCCESSFUL_LOGIN:  # only count successful logins
            user_logins[user_name] = user_logins.get(user_name, 0) + 1  # count the number of logins for each user

    most_freq_user = max(user_logins, key=lambda user: user_logins[user])
    least_freq_user = min(user_logins, key=lambda user: user_logins[user])

    return most_freq_user, least_freq_user
