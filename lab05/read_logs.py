import logging
import sys

from extract_data import *
from msg_type_utils import *

logger = logging.getLogger()

logger.setLevel(logging.CRITICAL)

stdout_handler = logging.StreamHandler(sys.stdout)
stderr_handler = logging.StreamHandler(sys.stderr)

stdout_handler.setLevel(logging.DEBUG)
stderr_handler.setLevel(logging.ERROR)

formatter = logging.Formatter('%(levelname)s: %(message)s')
stdout_handler.setFormatter(formatter)
stderr_handler.setFormatter(formatter)

logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)


def read_logs_from_file(file_name: str):
    try:
        with open(file_name, 'r') as file:
            for line in file:
                log_entry = extract_data(line.strip())
                if log_entry:
                    total_bytes = len(line.encode('utf-8'))
                    logging.debug(f'Total amount of bytes: {total_bytes}')
                    analyze_msg_type(log_entry, logger)
                    yield log_entry
    except FileNotFoundError:
        print(f"File {file_name} not found.")


