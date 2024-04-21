import random
import datetime
from typing import List, Tuple, Iterable
import statistics

from extract_data import LogEntry
from get_from_log import get_user_from_log
from msg_type_utils import get_msg_type, MessageType


# a) zwraca n logów z losowo wybranego użytkownika
def get_random_user_logs(logs: Iterable[LogEntry], n: int) -> List[LogEntry]:
    users_with_logs = list(filter(lambda log: get_user_from_log(log) is not None, logs))
    user_name = get_user_from_log(random.choice(users_with_logs))

    user_logs = [log for log in logs if get_user_from_log(log) == user_name]
    return random.sample(user_logs, min(n, len(user_logs)))


# b) oblicza średni czas trwania i odchylenie standardowe czasu trwania połączeń SSH
#   I. globalnie, dla całego pliku z logami,
#   II. dla każdego użytkownika niezależnie.

def get_avg_duration_and_deviation(logs: Iterable[LogEntry]) -> Tuple[float, float]:
    session_starts: dict[int, str] = {}
    session_durations = []

    for log in logs:
        if "session opened" in log.event_description:
            session_starts[log.pid] = log.timestamp

        elif "session closed" in log.event_description and log.pid in session_starts:
            start_time = session_starts.pop(log.pid, None)
            if start_time:
                start_ = datetime.datetime.strptime(start_time, "%b %d %H:%M:%S")
                end_ = datetime.datetime.strptime(log.timestamp, "%b %d %H:%M:%S")
                duration = (end_ - start_).total_seconds()
                session_durations.append(duration)

    if session_durations:
        average_duration = statistics.mean(session_durations)
        std_deviation = (statistics.stdev(session_durations) if len(session_durations) > 1 else 0.0)
        return average_duration, std_deviation
    else:
        return 0.0, 0.0


def get_stats_grouped_by_user(logs: Iterable[LogEntry]) -> dict[str, Tuple[float, float]]:
    user_stats: dict[str, tuple[float, float]] = {}

    users = set([get_user_from_log(log) for log in logs])

    for user in users:
        user_logs = [log for log in logs if get_user_from_log(log) == user]
        user_stats[user] = get_avg_duration_and_deviation(user_logs)

    return user_stats


# c) Oblicza użytkowników, którzy logowali się najrzadziej i najczęściej.
def get_most_and_least_frequent_users(logs: Iterable[LogEntry]):
    user_logins: dict[str, int] = {}

    for log in logs:
        user_name = get_user_from_log(log)
        if user_name and get_msg_type(log) == MessageType.SUCCESSFUL_LOGIN:
            user_logins[user_name] = user_logins.get(user_name, 0) + 1

    most_freq_user = max(user_logins, key=lambda user: user_logins[user])
    least_freq_user = min(user_logins, key=lambda user: user_logins[user])

    return most_freq_user, least_freq_user


