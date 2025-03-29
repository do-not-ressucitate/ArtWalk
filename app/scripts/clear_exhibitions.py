# app/scripts/clear_exhibitions.py

import os
import csv
from datetime import datetime

FILE_PATH = "data/exhibitions_today.csv"
LOG_PATH = "data/exhibitions_log.txt"

def clear_csv():
    try:
        with open(FILE_PATH, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["title", "gallery_name", "address", "lat", "lon", "url"])  # headers
        log_message("✔ CSV cleared successfully.")
    except Exception as e:
        log_message(f"✘ Failed to clear CSV: {str(e)}")

def log_message(message):
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"[{datetime.utcnow()} UTC] {message}\n")

if __name__ == "__main__":
    clear_csv()