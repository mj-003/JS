import sys
from helpers import is_from_country


def requests_from_poland():
    for line in sys.stdin:
        if is_from_country(line, "pl"):
            sys.stdout.write(line)


if __name__ == "__main__":
    requests_from_poland()
