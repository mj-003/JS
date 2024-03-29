import sys
from helpers import find_largest_resource


if __name__ == "__main__":
    path, max_size = find_largest_resource(sys.stdin)
    print(f"Largest resource path: {path}, size: {max_size} GB")
