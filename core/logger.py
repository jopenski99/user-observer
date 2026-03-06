import json
import time
from datetime import datetime
from pathlib import Path
from threading import Thread, Lock

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

buffer = []
lock = Lock()


def get_log_file():
    date = datetime.now().strftime("%m-%d-%Y")
    return LOG_DIR / f"{date}.json"


def add_event(event):
    with lock:
        buffer.append(event)


def writer():
    while True:
        time.sleep(5)

        with lock:
            if not buffer:
                continue

            events = buffer.copy()
            buffer.clear()

        logfile = get_log_file()

        with open(logfile, "a", encoding="utf8") as f:
            for e in events:
                f.write(json.dumps(e) + "\n")


def start_logger():
    Thread(target=writer, daemon=True).start()