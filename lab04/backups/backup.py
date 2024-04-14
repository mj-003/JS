""" task05_a: Write a Python script that creates a backup of a directory"""

import subprocess
import sys
from datetime import datetime

from utils import *


def create_backup(src_directory: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    dirname = os.path.basename(os.path.normpath(src_directory))
    backup_dir = get_backup_dir()
    ext = ".tar.gz"

    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    backup_name = f"{timestamp}-{dirname}{ext}"
    backup_path = os.path.join(backup_dir, backup_name)
    os.chdir(os.path.dirname(src_directory))

    # Creating the archive using tar
    subprocess.run(["tar", "-czf", backup_path, dirname])

    # Writing to history
    record = {
        "date": datetime.now().isoformat(),
        "location": os.path.abspath(src_directory),
        "backup_file": backup_name,
    }
    write_to_history(record)

    print(f"File backup created: {backup_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python backup.py <directory-path>")
        sys.exit(1)

    source_directory: str = sys.argv[1]
    create_backup(source_directory)
