def sort_log(log_entries, index_key):
    if 0 > index_key > len(log_entries[0]):
        print("Not valid key.")
        return None
    return sorted(log_entries, key=lambda x: x[index_key])


