from time import sleep
import keyboard
import websocket
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler 
import threading
import logging
from subprocess import call
from infi.systray import SysTrayIcon
from config_class import config
from sys import exit as ex


#Setup logger with format 
# DATE TIME - PID - LogLevel - Message
logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S', filename='./logs/app.log', filemode='w')    
logger = logging.getLogger()

def keyPress(profile):
    logger.info(f'hotkey pressed {profile}')
    try:
        ws = websocket.WebSocket()
        try:
            ws.connect("ws://localhost:6805/client")
        except Exception as e:
            logger.error(e)
        logger.info(f'Sending profile change request {profile}')
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

def verifyConnection(systray):
    try:
        websocket.WebSocket().connect("ws://localhost:6805/client")    
    except ConnectionRefusedError as e:
        logger.error(e)

def startServer():
    call('node ./goxlr.js', shell=False)
    print("server started")

def observe():
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()     
    
def main():
    try:
        menu_options = (("Verify Connection", None, verifyConnection),("Reload Config", None, config.loadConfig), ("Exit", None, exit))
        systray = SysTrayIcon("./icon.ico", "Example tray icon", menu_options)
        systray.start()
        logger.info("Created system tray.")
        obsThread = threading.Thread(target=observe)
        obsThread.daemon = True
        obsThread.start()
        #Try to start websocket server
        nodeThread = threading.Thread(target=startServer, daemon=True)
        print("starting server...")
        nodeThread.start()
        logger.info("Listening for hotkeys...")
        print("Press ESC to stop.")
        keyboard.wait('esc')        
    except KeyboardInterrupt as e:
        logger.error(e)       
    finally:
        systray.shutdown()
        ex("exiting")    

if __name__ == "__main__":
    main()


