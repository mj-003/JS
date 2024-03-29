import sys
from helpers import get_code_response


def code_200_write():
    for line in sys.stdin:
        if get_code_response(line) == '200':
            sys.stdout.write(line)


if __name__ == "__main__":
    code_200_write()
