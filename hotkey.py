import keyboard
import websocket
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler 
import threading

from config_class import config



class Event(LoggingEventHandler):
    def dispatch(self, event):
        if event.src_path == ".\config.toml" and event.event_type == "modified":
            conf.loadConfig()



def keyPress(profile):
    print(f'hotkey pressed {profile}')
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:6805/client")
    ws.send(f'changeprofile={profile}')
    print(ws.recv())
    ws.close()

def observe():
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()      


conf = config("./config.toml", keyPress)


def main():
    obsThread = threading.Thread(target=observe)
    obsThread.start()
    
    print("Press ESC to stop.")
    keyboard.wait('esc')

if __name__ == "__main__":
    main()


