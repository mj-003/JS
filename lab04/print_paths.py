""" task 2a: Write a Python script that prints all directories or directories and
    executable files  in the PATH environment variable."""

import argparse
import os

path = os.environ['PATH'] if 'PATH' in os.environ else ""   # Get the PATH environment variable
directories = path.split(os.pathsep)    # Get a list of directories in the PATH


# (2a) Print all directories in the PATH environment variable
def print_paths_directories():
    for directory in directories:
        if os.path.exists(directory):  # Check if the directory exists
            print(directory)


# (2b) Print all directories and list of executable files
def print_paths_executables():
    for directory in directories:
        if os.path.exists(directory):
            files = os.listdir(directory)       # List all files in the directory
            executables = [
                # Check if the file is executable
                file for file in files if os.access(os.path.join(directory, file), os.X_OK)
            ]
            print(directory)
            for executable in executables:
                print(f'  {executable}')


# Parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(
        description='Print the directories and executables in the PATH environment variable')
    parser.add_argument('action', choices=['directories', 'executables'],
                        help='Action to perform: directories or executables')
    arguments = parser.parse_args()
    return arguments


if __name__ == '__main__':
    args = parse_args()

    if args.action == 'directories':
        print_paths_directories()

    elif args.action == 'executables':
        print_paths_executables()

    else:
        print("Please provide a valid action: directories or executables.")
