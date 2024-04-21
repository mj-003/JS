import logging
import typer
from enum import Enum
from brute_force import *
from calculate_stats import *
from cli import Command
from msg_type_utils import get_msg_type
from read_logs import read_logs_from_file

logger = logging.getLogger(__name__)


class LogLevels(str, Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    DEBUG = "DEBUG"
    CRITICAL = "CRITICAL"


app = typer.Typer(help="SSH log analyzer")
app.logfile_path = None  # Attribute to store the logfile path


@app.callback()
def main(
        logfile: str = "/Users/m_juchiewicz/Desktop/studia/semestr-4/JS/lab05/data/OpenSSH_2k.log",
        loglevel: LogLevels = LogLevels.DEBUG
):
    """
    Set up the logfile path and log level.
    """
    app.logfile_path = logfile
    logging.basicConfig(level=logging.getLevelName(loglevel))


@app.command(Command.IPV4S.value)
def get_ipv4s():
    """
    Get all IPv4 addresses from the logs.
    """
    logs = read_logs_from_file(app.logfile_path)
    for log in logs:
        typer.echo(get_ipv4_from_log(log))


@app.command(Command.USER.value)
def get_usernames():
    """
    Get all usernames from the logs.
    """
    logs = read_logs_from_file(app.logfile_path)
    for log in logs:
        user = get_user_from_log(log)
        if user:
            typer.echo(user)


@app.command(Command.MSG_TYPE.value)
def get_message_types():
    """
    Get all message types from the logs.
    """
    logs = read_logs_from_file(app.logfile_path)
    for log in logs:
        typer.echo(get_msg_type(log))


@app.command(Command.GET_RANDOM_LOGS.value)
def get_global_stats():
    """
    Get random logs from random users.
    """
    logs = read_logs_from_file(app.logfile_path)
    typer.echo(get_avg_duration_and_deviation(logs))


@app.command('stats_grouped_by_user')
def get_user_stats_by_user():
    """
    Get the average session duration and standard deviation.
    """
    logs = read_logs_from_file(app.logfile_path)
    typer.echo(get_stats_grouped_by_user(logs))


@app.command('most_least_frequent_users')
def get_most_least_frequent():
    """
    Get the most and least frequent users.
    """
    logs = read_logs_from_file(app.logfile_path)
    typer.echo(get_most_and_least_frequent_users(logs))


@app.command('brute_force')
def get_brute_force_attempts(
        interval: int = typer.Option(300, help="Interval in seconds for brute force detection"),
        user: bool = typer.Option(False, help="Enable to detect brute force attempts for a single user"),
):
    """
    Get the brute force attempts.
    :param interval: The interval in seconds.
    :param user: Enable to detect brute force attempts for a single user.
    """
    logs = read_logs_from_file(app.logfile_path)
    typer.echo(detect_bruteforce(logs, interval, user))


@app.command('random_user_logs')
def get_random_user_logs():
    """
    Get random logs from random users.
    """
    logs = read_logs_from_file(app.logfile_path)
    random_user = get_random_user_logs(logs)
    for log in random_user:
        typer.echo(log)


if __name__ == '__main__':
    app()
