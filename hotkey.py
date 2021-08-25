import websocket
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler 
import threading
import logging
from subprocess import Popen, PIPE
from config_class import config
from sys import exit as ex
from os import mkdir, path
from pathlib import Path
from ui import userInterface
from shutil import which

goXlrDir = str(Path.home()) + '\\Documents\\GoXLRPlugin\\'
#Setup logger with format 
# DATE TIME - PID - LogLevel - Message
try:
    logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S', filename=goXlrDir + 'logs\\app.log', filemode='w')    
except FileNotFoundError:
    if not path.isdir(goXlrDir):
        mkdir(goXlrDir)
    mkdir(goXlrDir + 'logs')
    logging.basicConfig(format='%(asctime)s - %(process)d - %(levelname)s - %(message)s', level=logging.INFO, datefmt='%d-%b-%y %H:%M:%S', filename=goXlrDir + 'logs\\app.log', filemode='w')    
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

try:
    conf = config(keyPress, goXlrDir + 'config.toml')
except FileNotFoundError:
    with open(goXlrDir + 'config.toml', 'w') as file:
        file.write("""# Define keys to be pressed in parallel array with profiles.
# ex. keys=["F1", "F2"]
#     profiles=["profile1", "profile2"]\n
# This will set profile1 when you press F1 and set profile2 when press F2

title = "GoXLR Streamdeck Emulator"\n

[Server]
GoXLRAddress="ws://localhost:6805/?GoXLRApp"
ClientAddress="ws://localhost:6805/client="

[Hotkeys]
keys=["F13", "CTRL + B"]
profiles=["Desk", "Game"] 
""")
    conf = config(keyPress, goXlrDir + 'config.toml')

class Event(LoggingEventHandler):
    def dispatch(self, event):
        if event.src_path == goXlrDir + "config.toml" and event.event_type == "modified":
                conf.loadConfig()

def verifyConnection(systray):
    try:
        websocket.WebSocket().connect("ws://localhost:6805/client")    
    except ConnectionRefusedError as e:
        logger.error(e)

def startServer():
    try:
        process = Popen([which("node"), 'C:\\Users\\Ryan\\Documents\\GoXLR-Streamdeck-Plugin\\goxlr.js'])
        if process.poll() == None:
            print("started")
    except Exception as e:
        print(e)
    
def observe():
    event_handler = Event()
    observer = Observer()
    observer.schedule(event_handler, ".", recursive=True)
    observer.start()     
    
def main():
    try:
        #TO DO -- Implement UI
        obsThread = threading.Thread(target=observe, daemon=True)
        obsThread.start()
        #Try to start websocket server
        print("starting server...")
        """ nodeThread = threading.Thread(target=startServer, daemon=True)
        nodeThread.start() """
        startServer()
        logger.info("Listening for hotkeys...")
        print("Press ESC to stop.")
        ui = userInterface(goXlrDir)
    except KeyboardInterrupt as e:
        logger.error(e)       
    finally:
        ex("exiting")    

if __name__ == "__main__":
    main()


