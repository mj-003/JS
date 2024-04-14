""" task03: Write a Python script that is a simple implementation of the tail
    command in Unix-like systems."""

import argparse
import os
import time
from collections import deque


# Function to print the last N lines of a file
def tail(file_name: str, lines: int = 10) -> None:
    try:
        with open(file_name, 'r') as file:
            lines = deque(file, lines)
            for line in lines:
                print(line, end='')
    except FileNotFoundError:
        print(f'{file_name}: No such file or directory')


# Function to print the last N lines and follow a file
def follow(file_name: str, lines: int = 10) -> None:
    try:
        with open(file_name, 'r') as file:
            tail(file_name, lines)
            file.seek(0, os.SEEK_END)   # Move the cursor to the end of the file
            while True:
                current_position = file.tell()  # Get the current position of the cursor
                line = file.readline()
                if not line:
                    time.sleep(0.1)  # If there is no new line, wait for 0.1 seconds
                    current_size = os.stat(file_name).st_size  # Get the current size of the file
                    if current_size > current_position:  # Check if the file has been updated
                        file.seek(current_position)  # Move the cursor to the last position
                else:
                    print(line, end='')
    except FileNotFoundError:
        print(f'{file_name}: No such file or directory')


def parse_args():
    parser = argparse.ArgumentParser(description='Print the last N lines of a file')
    parser.add_argument('filename', nargs='?', help='File to read')
    parser.add_argument('-n', '--lines', type=int, default=10, help='Number of lines to print')
    parser.add_argument('-f', '--follow', action='store_true', help='Follow the file')
    arguments = parser.parse_args()
    return arguments


if __name__ == '__main__':
    args = parse_args()

    if args.filename:
        if args.follow:
            follow(args.filename, args.lines)
        else:
            tail(args.filename, args.lines)
    else:
        print("Please provide a filename.")
