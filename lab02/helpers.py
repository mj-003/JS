from extractors import *


def count_http_response(code, logs):
    count = 0
    for line in logs:
        if get_code_response(line) == str(code):
            count += 1
    return count


def bytes_sum(logs):
    total = 0
    for line in logs:
        total += get_bytes(line)
    return total


def is_graphic(line):
    graphic_extensions = ['gif', 'jpg', 'jpeg', 'xbm']
    if get_extension(line) in graphic_extensions:
        return True
    else:
        return False


def is_between_hours(line, start_hour, end_hour):
    hour = get_hour(line)
    minutes = get_minutes(line)
    seconds = get_seconds(line)
    if start_hour <= hour or hour < end_hour or (hour == end_hour and minutes == seconds == 0):
        return True
    else:
        return False


def is_specific_day(line, day):
    if get_day(line) == day:
        return True
    else:
        return False


def is_from_country(line, country):
    if get_country(line) == country:
        return True
    else:
        return False


def count_resources(logs):
    graphic_count = 0
    other_count = 0
    for line in logs:
        if is_graphic(line):
            graphic_count += 1
        else:
            other_count += 1
    return graphic_count, other_count


def find_largest_resource(logs):
    max_size = 0
    path = ''
    for line in logs:
        bytes_from_line = get_bytes(line)
        if bytes_from_line > max_size:
            max_size = bytes_from_line
            path = get_path(line)
    return path, max_size
