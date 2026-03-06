import time
from datetime import datetime
from core.event_bus import publish

IDLE_THRESHOLD = 300  # 5 minutes

last_input_time = time.time()
is_idle = False


def register_input():
    global last_input_time, is_idle

    last_input_time = time.time()

    if is_idle:
        is_idle = False

        publish({
            "timestamp": datetime.utcnow().isoformat(),
            "event": "idle_end"
        })


def check_idle():

    global is_idle

    if not is_idle and time.time() - last_input_time > IDLE_THRESHOLD:

        is_idle = True

        publish({
            "timestamp": datetime.utcnow().isoformat(),
            "event": "idle_start"
        })