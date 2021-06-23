from typing import AnyStr
import keyboard
import websocket
import toml
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler 
import threading
import logging

class Event(LoggingEventHandler):
    def dispatch(self, event):
        if event.src_path == ".\config.toml" and event.event_type == "modified":
            print(f'event type: {event.event_type}  path : {event.src_path}')

def keyPress():
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:6805/client")
    ws.send("changeprofile=Desk")
    print(ws.recv())
    ws.close()

def debugPress():
    print("pressed hotkey")

def observe():
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()


obsThread = threading.Thread(target=observe)

obsThread.start()


config = toml.load("./config.toml")
keys = config["Hotkeys"]

for key in keys["keys"]:
    keyboard.add_hotkey(key, debugPress) #<-- attach the function to hot-key

print("Press ESC to stop.")
keyboard.wait('esc')
