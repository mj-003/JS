import sys
from helpers import count_http_response

if __name__ == "__main__":
    print(f"Code 200 request count: {count_http_response(200, sys.stdin)}")
