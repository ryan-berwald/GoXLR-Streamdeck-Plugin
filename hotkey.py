import keyboard
import websocket
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler 
import threading
import logging
import subprocess
from infi.systray import SysTrayIcon
from config_class import config


#Setup logger with format 
# DATE TIME - PID - LogLevel - Message
logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S', filename='app.log', filemode='w')    
logger = logging.getLogger()

def keyPress(profile):
    logger.info(f'hotkey pressed {profile}')
    try:
        ws = websocket.WebSocket()
        ws.connect("ws://localhost:6805/client")
        ws.send(f'changeprofile={profile}')
        logger.info(ws.recv())
    except Exception as e:
        logger.error(e)
    finally:
        ws.close()


conf = config(keyPress, "./config.toml")

class Event(LoggingEventHandler):
    def dispatch(self, event):
        if event.src_path == ".\config.toml" and event.event_type == "modified":
                conf.loadConfig()

def connect(systray):
    try:
        websocket.WebSocket().connect("ws://localhost:6805/client")    
    except ConnectionRefusedError as e:
        logger.error(e)


def observe():
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()      
    
def main():
    menu_options = (("Say Hello", None, connect),)
    systray = SysTrayIcon("icon.ico", "Example tray icon", menu_options)
    systray.start()
    logger.info("Created tray menu.")
    obsThread = threading.Thread(target=observe)
    obsThread.start()
    subprocess.call('node ./goxlr.js', shell=True)
    logger.info("Listening for hotkeys...")
    print("Press ESC to stop.")
    keyboard.wait('esc')
    logger.info("Exiting.", exit)

if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        # this log will include traceback
        logger.exception('function_will_exit failed with exception')
        # this log will just include content in sys.exit
        logger.error(str(e))
        # if you don't need exception traceback from Python
        # os._exit(1)
        raise



