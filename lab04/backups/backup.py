""" task05_a: Write a Python script that creates a backup of a directory"""

import subprocess
import sys
from datetime import datetime

from utilities import *


def create_backup(src_directory: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dirname = os.path.basename(os.path.normpath(src_directory))
    backup_dir = get_backup_dir()
    ext = ".tar.gz"

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    backup_name = f"{timestamp}-{dirname}{ext}"
    backup_path = os.path.join(backup_dir, backup_name)

    # Creating the archive using tar
    # c: create a new archive
    # z: compress the archive using gzip
    # f: specify the filename of the archive
    # -C: change to the directory before processing the following arguments

    subprocess.run(["tar", "-czf", backup_path, "-C", os.path.dirname(src_directory), dirname])

    # Write the backup record to the history file
    write_to_history(src_directory, backup_name)

    print(f"File backup created: {backup_path}")


# Write the backup record to the history file
def write_to_history(src_directory, backup_name) -> None:
    backup_dir = get_backup_dir()
    history_file_path = os.path.join(backup_dir, "backup_history.json")

    if not os.path.exists(history_file_path):
        with open(history_file_path, "w") as file:
            json.dump([], file)

    record = {
        "date": datetime.now().isoformat(),
        "location": os.path.abspath(src_directory),
        "backup_file": backup_name,
    }

    with open(history_file_path, "r+") as file:
        history = json.load(file)
        history.append(record)
        file.seek(0)
        json.dump(history, file, indent=4)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Wrong number of arguments.")
        sys.exit(1)

    source_directory: str = sys.argv[1]
    create_backup(source_directory)
