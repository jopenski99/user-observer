import win32gui
import win32process
import psutil

last_window = None


def get_active_app():

    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)

    _, pid = win32process.GetWindowThreadProcessId(hwnd)

    try:
        process = psutil.Process(pid)
        app = process.name()
    except:
        app = "unknown"

    return app, title