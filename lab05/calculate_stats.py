from collections import defaultdict
from random import random
from typing import List, Tuple
import statistics

from extract_data import LogEntry
from get_from_log import get_user_from_log


# a) zwraca n logów z losowo wybranego użytkownika
def get_random_user_logs(logs: List[LogEntry], n: int) -> List[LogEntry]:
    users_with_logs = filter(lambda log: get_user_from_log(log.event_description) is not None, logs)
    user = random.choice(list(users_with_logs))

    user_logs = [log for log in logs if get_user_from_log(log.event_description) == get_user_from_log(user)]
    return random.sample(user_logs, min(n, len(user_logs)))


# b) oblicza średni czas trwania i odchylenie standardowe czasu trwania połączeń SSH
#   I. globalnie, dla całego pliku z logami,
#   II. dla każdego użytkownika niezależnie.

def get_users_sessions(logs: List[LogEntry]) -> dict[str, Tuple[List[int], float, float]]:
    user_sessions = defaultdict(list)

    for log in logs:
        user = get_user_from_log(log.event_description)
        if "session opened" in log.event_description:
            user_sessions[user].append(log.timestamp)
        elif "session closed" in log.event_description:
            starts = user_sessions[user]
            if starts:
                start = starts.pop()
                duration = (log.timestamp - start).total_seconds()
                user_sessions[user].append(duration)

    user_durations = {}
    for user, durations in user_sessions.items():
        session_durations = durations[1::2]
        if session_durations:
            mean_duration = statistics.mean(session_durations)
            std_duration = statistics.stdev(session_durations)
            user_durations[user] = (session_durations, mean_duration, std_duration)

    return user_durations


def get_stats_for_all(logs: List[LogEntry]) -> Tuple[float, float]:
    users_durations = get_users_sessions(logs)
    all_durations = [duration for durations, _, _ in users_durations.values() for duration in durations]
    return statistics.mean(all_durations), statistics.stdev(all_durations)


def get_stats_for_user(logs: List[LogEntry], user: str) -> tuple:
    users_durations = get_users_sessions(logs)
    return users_durations[user][1:]


# c) Oblicza użytkowników, którzy logowali się najrzadziej i najczęściej.

def get_least_frequent_users(logs: List[LogEntry]) -> List[str]:
    users_sessions = get_users_sessions(logs)
    min_sessions = min(len(sessions) for sessions, _, _ in users_sessions.values())
    return [user for user, (sessions, _, _) in users_sessions.items() if len(sessions) == min_sessions]


def get_most_frequent_users(logs: List[LogEntry]) -> List[str]:
    users_sessions = get_users_sessions(logs)
    max_sessions = max(len(sessions) for sessions, _, _ in users_sessions.values())
    return [user for user, (sessions, _, _) in users_sessions.items() if len(sessions) == max_sessions]
