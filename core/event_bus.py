from queue import Queue

event_queue = Queue()

def publish(event):
    event_queue.put(event)

def consume():
    return event_queue.get()