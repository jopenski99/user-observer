import time
import atexit
from core.event_bus import publish
from core.logger import add_event, start_logger
from datetime import datetime
from pynput import keyboard, mouse

from core.logger import add_event, start_logger
from core.activity_tracker import register_input, check_idle
from app_tracker.windows import get_active_app

last_window = None


def log_window_change():
    global last_window

    app, title = get_active_app()
    current = f"{app}:{title}"

    if current != last_window:

        last_window = current

        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": "window_change",
            "app": app,
            "window": title
        }

        add_event(event)


def on_key_release(key):

    register_input()

    app, title = get_active_app()

    publish({
        "timestamp": datetime.utcnow().isoformat(),
        "event": "keyboard",
        "key": str(key),
        "app": app,
        "window": title
    })

def on_click(x, y, button, pressed):

    if pressed:

        register_input()

        app, title = get_active_app()

        publish({
            "timestamp": datetime.utcnow().isoformat(),
            "event": "mouse_click",
            "button": str(button),
            "x": x,
            "y": y,
            "app": app,
            "window": title
        })



def end_session():
    publish({
        "timestamp": datetime.utcnow().isoformat(),
        "event": "session_end"
    })

atexit.register(end_session)

def main():

    print("User monitor started")
    publish({
        "timestamp": datetime.utcnow().isoformat(),
        "event": "session_start"
    })
    start_logger()

    keyboard.Listener(on_release=on_key_release).start()
    mouse.Listener(on_click=on_click).start()

    while True:

        log_window_change()
        check_idle()

        time.sleep(1)


if __name__ == "__main__":
    main()