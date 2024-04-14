""" task 2a: Write a Python script that prints all directories or directories and
    executable files  in the PATH environment variable."""

import argparse
import os

path = os.environ['PATH'] if 'PATH' in os.environ else ""
directories = path.split(os.pathsep)


# (2a) Print all directories in the PATH environment variable
def print_paths_directories():
    for directory in directories:
        if os.path.exists(directory):  # Check if the directory exists
            print(directory)


# (2b) Print all directories and list of executable files
def print_paths_executables():
    for directory in directories:
        if os.path.exists(directory):
            files = os.listdir(directory)
            executables = [
                file for file in files if os.access(os.path.join(directory, file), os.X_OK)
            ]
            print(directory)
            for executable in executables:
                print(f'  {executable}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print directories and executables in the PATH environment variable')
    parser.add_argument('action', choices=['directories', 'executables'], help='Action to perform: directories or '
                                                                               'executables')
    args = parser.parse_args()

    if args.action == 'directories':
        print_paths_directories()

    elif args.action == 'executables':
        print_paths_executables()
