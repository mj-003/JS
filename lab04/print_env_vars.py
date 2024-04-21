""" task 1: Write a Python script that prints all environment variables
    that contain a given keyword in alphabetic order."""

import os
import sys


# Filter environment variables by keywords
def filter_env_vars(keywords=None):
    if not keywords:
        return os.environ.keys()
    # Return a list of environment variables that contain any of the keywords
    return sorted([env for env in os.environ if any(keyword in env for keyword in keywords)])


# Print environment variables
def print_env_vars(env_vars):
    for env_var in env_vars:
        print(f'{env_var} = {os.environ[env_var]}')


if __name__ == '__main__':
    my_keywords = sys.argv[1:]  # Get the keywords from the command line
    filtered_env_vars = filter_env_vars(my_keywords)
    print_env_vars(filtered_env_vars)
