""" task04: Write a Python script that takes a directory path as an argument
    and calculates statistics for all files in that directory."""

import subprocess
import os
import sys
import json


# Calculate statistics for a given file
def calculate_stats(file_path):
    try:
        output = subprocess.check_output(["java", "Main", file_path], text=True)
        lines = output.strip().split("\n")
        headers = lines[0].split(",")
        values = lines[1].split(",")
        file_stats = dict(zip(headers, values))
        return file_stats
    except subprocess.CalledProcessError as e:
        print(f"Error processing file {file_path}: {e}")
        return None


# Get statistics for all files in a directory
def get_stats(directory_path):
    files_stats = []

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                file_stats = calculate_stats(file_path)
                if file_stats:
                    files_stats.append(file_stats)

    return files_stats


# Get summary statistics for all files
def get_summary_stats(files_stats):
    summary_stats = {"Total files": len(files_stats),
                     "Total lines": sum(int(stats["Total Lines"]) for stats in files_stats),
                     "Total words": sum(int(stats["Total Words"]) for stats in files_stats),
                     "Total chars": sum(int(stats["Total Characters"]) for stats in files_stats),
                     "Most frequent word": max((stats["Most Frequent Word"] for stats in files_stats), key=len),
                     "Most frequent char": max((stats["Most Frequent Character"] for stats in files_stats), key=len)}
    return summary_stats


def main():
    if len(sys.argv) != 2:
        print("No directory path provided.")
        sys.exit(1)
    directory_path = sys.argv[1]

    files_stats = get_summary_stats(get_stats(directory_path))
    if files_stats:
        print("Results:")
        print(json.dumps(files_stats, indent=4))


if __name__ == "__main__":
    main()
