""" task05_b: Write a Python script that restores a backup of a directory"""

import shutil
import subprocess
import sys
from typing import List

from utilities import *


# Function to list all backups
def list_backups() -> List[Dict[str, str]]:
    backup_dir = get_backup_dir()
    history_file_path = os.path.join(backup_dir, "backup_history.json")
    with open(history_file_path, "r") as file:
        history = json.load(file)
    return history


# Function to restore a backup
def restore_backup(target_directory: str, backup_number: int) -> None:
    backups_history = list_backups()
    if backup_number < 0 or backup_number >= len(backups_history):
        print("Invalid backup number.")
        return

    backup_record = backups_history[backup_number]
    backup_file = os.path.join(get_backup_dir(), backup_record["backup_file"])

    # Clearing the target directory
    for filename in os.listdir(target_directory):
        file_path = os.path.join(target_directory, filename)  # Get the full path
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)  # Remove the file
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  # Remove the directory

    # Extracting the archive
    # x: extract files from an archive
    # z: filter the archive through gzip
    # f: use archive file
    # -C: change to the directory before processing the following arguments

    subprocess.run(["tar", "-xzf", backup_file, "-C", target_directory])
    print(f"Restored {backup_file} to {target_directory}")


if __name__ == "__main__":
    target_directory: str = (
        sys.argv[1] if len(sys.argv) >= 2 else get_backup_dir()
    )
    history = list_backups()
    for i, record in enumerate(reversed(history)):
        print(f"{i}: {record['date']} - {record['backup_file']}")

    backup_number: int = int(input("Enter the number of the backup to restore: "))
    restore_backup(target_directory, backup_number)
