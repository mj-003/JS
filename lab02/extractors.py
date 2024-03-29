from datetime import datetime


def get_host_name(line):
    try:
        return line.split()[0]
    except IndexError:
        return ""


def get_date(line):
    try:
        return line.split()[3][1:12]
    except IndexError:
        return ""



def get_time(line):
    try:
        return line.split()[3][13:21]
    except IndexError:
        return ""


def get_path(line):
    try:
        return line.split()[6]
    except IndexError:
        return ""


def get_code_response(line):
    try:
        return line.split()[-2]
    except IndexError:
        return ""


def get_bytes(line):
    try:
        bytes_from_line = line.split()[-1]
        if bytes_from_line.isdigit():
            return int(bytes_from_line)
        else:
            return 0
    except IndexError or ValueError:
        return 0


def get_extension(line):
    try:
        return get_path(line).split('.')[-1]
    except IndexError:
        return ""


def get_hour(line):
    try:
        return int(get_time(line).split(':')[0])
    except IndexError or ValueError:
        return 0


def get_minutes(line):
    try:
        return int(get_time(line).split(':')[1])
    except IndexError or ValueError:
        return 0


def get_seconds(line):
    try:
        return int(get_time(line).split(':')[2])
    except IndexError:
        return 0


def get_day(line):
    try:
        date = datetime.strptime(get_date(line), "%d/%b/%Y").date()
        return date.weekday()
    except ValueError:
        return ""


def get_country(line):
    try:
        return get_host_name(line).split('.')[-1]
    except IndexError:
        return ""
