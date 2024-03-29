import sys


def read_file():
    for line in sys.stdin:
        sys.stdout.write(line)
    sys.stdout.flush()


if __name__ == "__main__":
    read_file()
