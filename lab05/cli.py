import logging

from brute_force import detect_bruteforce
from read_logs import read_logs_from_file
from get_from_log import *
from calculate_stats import *
from msg_type_utils import get_msg_type
import argparse
from enum import Enum


class Command(Enum):
    IPV4S = "ipv4s"
    USER = "user"
    MSG_TYPE = "message_type"
    GET_RANDOM_LOGS = "get_random_logs"
    STATS = "stats"
    MOST_AND_LEAST_FREQUENT_USERS = "most_and_least_frequent_users"
    BRUTE_FORCE = "brute_force"


def main():
    parser = argparse.ArgumentParser(description="SSH Log Analyzer")

    # arguments
    parser.add_argument("logfile", help="Path to the SSH log file")
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Set the logging level",
        default="INFO",
    )

    # subparsers
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    subparsers.add_parser(Command.IPV4S.value, help="Get all IPv4 from logs in file")
    subparsers.add_parser(Command.USER.value, help="Get all users from logs in file")
    subparsers.add_parser(Command.MSG_TYPE.value, help="Get all msg types from logs in file")

    random_users_parser = subparsers.add_parser(Command.GET_RANDOM_LOGS.value, help="Get random logs from random user")
    random_users_parser.add_argument("--count", type=int, default=10, help="Number of random logs to retrieve")

    stats_parser = subparsers.add_parser(Command.STATS.value,
                                         help="Get the average session duration and standard deviation")
    stats_parser.add_argument("--group-by-user", action="store_true", default=False, help="Group stats by user")

    subparsers.add_parser(Command.MOST_AND_LEAST_FREQUENT_USERS.value, help="Get the most and least frequent user")

    brute_force_parser = subparsers.add_parser(Command.BRUTE_FORCE.value, help="Get the brute force attempts")
    brute_force_parser.add_argument("--max-interval", type=int, default=100, help="Max interval between attempts")
    brute_force_parser.add_argument("--max-attempts", type=int, default=60, help="Max attempts")
    brute_force_parser.add_argument("--single-user", action="store_true", default=False, help="Single user")

    args = parser.parse_args()
    logs = read_logs_from_file(args.logfile)
    logger = logging.getLogger()

    match args.log_level:
        case "DEBUG":
            logger.setLevel(logging.DEBUG)
        case "INFO":
            logger.setLevel(logging.INFO)
        case "WARNING":
            logger.setLevel(logging.WARNING)
        case "ERROR":
            logger.setLevel(logging.ERROR)
        case "CRITICAL":
            logger.setLevel(logging.CRITICAL)

    match args.subcommand:
        case Command.IPV4S.value:
            for log in logs:
                print(get_ipv4_from_log(log))

        case Command.USER.value:
            for log in logs:
                print(get_user_from_log(log))

        case Command.MSG_TYPE.value:
            for log in logs:
                print(get_msg_type(log))

        case Command.GET_RANDOM_LOGS.value:
            random_user_logs = get_random_user_logs(logs, args.count)
            for log in random_user_logs:
                print(log)

        case Command.STATS.value:
            if args.group_by_user:
                print(get_stats_grouped_by_user(logs))
            else:
                print(get_avg_duration_and_deviation(logs))

        case Command.MOST_AND_LEAST_FREQUENT_USERS.value:
            print(get_most_and_least_frequent_users(logs))

        case Command.BRUTE_FORCE.value:
            detect_bruteforce(logs, args.max_interval, args.max_attempts, args.single_user)


if __name__ == "__main__":
    main()
