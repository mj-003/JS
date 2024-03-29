import sys
from helpers import is_between_hours


def between_22_6():
    for line in sys.stdin:
        if is_between_hours(line, 22, 6):
            sys.stdout.write(line)


if __name__ == "__main__":
    between_22_6()
