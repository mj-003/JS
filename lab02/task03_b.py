import sys
from helpers import bytes_sum
bytes_to_gb = 1024 ** 3


def total_gb_send():
    total = bytes_sum(sys.stdin)
    total_in_gb = total / bytes_to_gb
    return total_in_gb


if __name__ == "__main__":
    print(f"Data sent in GB: {total_gb_send():.2f}")
