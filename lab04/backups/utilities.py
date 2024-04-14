import os
import json
from typing import Dict


# Get the backup directory
def get_backup_dir() -> str:
    return os.environ.get(
        "BACKUPS_DIR", os.path.join(os.path.expanduser("~"), ".backups")
    )



