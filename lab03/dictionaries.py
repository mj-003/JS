# 3a
def entry_to_dict(log: tuple):
    log_dict = {
        "host_name": log[0],
        "date_time": log[1],
        "path": log[2],
        "status_code": log[3],
        "bytes": log[4]
    }
    return log_dict


# 3b
def log_to_dict(log_entries: list[tuple]) -> dict:
    log_dict = {}
    for log in log_entries:
        host_name = log[0]
        log_dict.setdefault(host_name, []).append(entry_to_dict(log))
    return log_dict


# 3c
def get_addrs(logs_dict: dict):
    return list(logs_dict.keys())


# 3d
def print_dict_entry_dates(logs_dict: dict):
    for host, entries in logs_dict.items():
        num_requests = len(entries)
        fst_request_date = min(entry['date_time'] for entry in entries)
        last_request_date = max(entry['date_time'] for entry in entries)
        num_200_requests = sum(1 for entry in entries if entry['status_code'] == 200)
        ratio = num_200_requests / num_requests if num_requests > 0 else 0

        print(f"Host name: {host}")
        print(f"Number of requests: {num_requests}")
        print(f"First request date: {fst_request_date}")
        print(f"Last request date: {last_request_date}")
        print(f"Ratio of successful requests: {ratio:.2f}")
        print("----------------------------------------")
