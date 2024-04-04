# 2c
def get_entries_by_addr(log_entries: list[tuple], addr: str):
    return [log for log in log_entries if log[0] == addr]


# 2d
def get_entries_by_code(log_entries: list[tuple], code: int):
    return [log for log in log_entries if log[3] == code]


# 2e
def get_failed_reads(log_entries: list[tuple], join=False):
    codes_4xx = [log for log in log_entries if 400 <= log[3] < 500]
    codes_5xx = [log for log in log_entries if 500 <= log[3] < 600]

    if join:
        return codes_4xx + codes_5xx
    else:
        return codes_4xx, codes_5xx


# 2f
def get_entries_by_extension(log_entries: list[tuple], extension: str):
    return [log for log in log_entries if log[2].endswith('.' + extension)]


# 2g
def print_entries(log_entries: list[tuple]):
    for log in log_entries:
        print(log)
