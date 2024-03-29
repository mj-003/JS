import sys
from helpers import count_resources

if __name__ == "__main__":
    graphic_count, other_count = count_resources(sys.stdin)
    try:
        print(f"Graphics download ratio: {graphic_count / other_count:.2f}")
    except ZeroDivisionError:
        print("No other than graphic files found")
