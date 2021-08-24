from time import sleep
import keyboard
import websocket
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler 
import threading
import logging
import subprocess
from infi.systray import SysTrayIcon
from config_class import config
from sys import exit as ex
from os import mkdir, path
from pathlib import Path

goXlrDir = str(Path.home()) + '\\Documents\\GoXLRPlugin\\'
#Setup logger with format 
# DATE TIME - PID - LogLevel - Message
try:
    logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S', filename=goXlrDir + '\\logs\\app.log', filemode='w')    
except FileNotFoundError:
    mkdir(goXlrDir + '\\Documents\\GoXLRPlugin\\logs')
    logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S', filename=goXlrDir + '\\logs\\app.log', filemode='w')    
finally:
    logger = logging.getLogger()
    
def keyPress(profile, keys):
    print("hotkey pressed")
    logger.info(f'hotkey pressed {profile}; {keys}')
    try:
        ws = websocket.WebSocket()
        try:
            ws.connect("ws://localhost:6805/client")
        except Exception as e:
            logger.error(e)
        logger.info(f'Sending profile change request {profile}')
        ws.send(f'changeprofile={profile}')
        #logger.info(ws.recv())
    except Exception as e:
        logger.error(e)
    finally:
        ws.close()

conf = config(keyPress, goXlrDir + '\\config.toml')

class Event(LoggingEventHandler):
    def dispatch(self, event):
        if event.src_path == goXlrDir + "\\config.toml" and event.event_type == "modified":
                conf.loadConfig()

def verifyConnection(systray):
    try:
        websocket.WebSocket().connect("ws://localhost:6805/client")    
    except ConnectionRefusedError as e:
        logger.error(e)

def startServer():
    print("server started")
    subprocess.call('node ./goxlr.js', shell=False)
    
def observe():
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()     
    
def main():
    try:
        menu_options = (("Verify Connection", None, verifyConnection),("Reload Config", None, config.loadConfig))
        systray = SysTrayIcon("./Assets/icon.ico", "Example tray icon", menu_options, on_quit=ex)
        systray.start()
        logger.info("Created system tray.")
        obsThread = threading.Thread(target=observe)
        obsThread.daemon = True
        obsThread.start()
        #Try to start websocket server
        print("starting server...")
        nodeThread = threading.Thread(target=startServer, daemon=True)
        nodeThread.start()
        logger.info("Listening for hotkeys...")
        print("Press ESC to stop.")
        keyboard.wait()        
    except KeyboardInterrupt as e:
        logger.error(e)       
    finally:
        systray.shutdown()
        nodeThread.join(3)
        obsThread.join(3)
        ex("exiting")    

if __name__ == "__main__":
    main()


