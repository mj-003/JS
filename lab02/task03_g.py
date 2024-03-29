import sys
from helpers import is_specific_day


def on_friday():
    for line in sys.stdin:
        if is_specific_day(line, 4):
            sys.stdout.write(line)


if __name__ == "__main__":
    on_friday()
