from time import sleep
import keyboard
import threading
import logging
from config_class import config
from sys import exit as ex
from os import mkdir, path, truncate
from pathlib import Path
from ui import userInterface
from Server import Server

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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

if not Path.is_file(Path(f'{goXlrDir}logs\\server.log')):
    with open(goXlrDir + "\\logs\\server.log", "w") as file:
        logger.info("Creating server log file")
        file.close()

def keyPress(profile, keys, server):
    print("hotkey pressed")
    logger.info(f'hotkey pressed {profile}; {keys}')
    try:
        print(server.ws.url)
        server.ws.send(f'changeprofile={profile}')
        print("sent data")
    except Exception as e:
        logger.error(e)





  

def main():
     
                
    ui = userInterface(goXlrDir)
    server = Server(ui)
    logger.info("Listening for hotkeys...")
    conf = config(keyPress, goXlrDir + "\\config.toml", goXlrDir, server)
    class Event(FileSystemEventHandler):
        def dispatch(self, event):
            print(event.src_path)
            if event.src_path == goXlrDir + "config.toml" and event.event_type == "modified": 
                conf.loadConfig(goXlrDir)
    def observe(conf):
        event_handler = Event()
        observer = Observer()
        observer.schedule(event_handler, goXlrDir, recursive=True)
        observer.start()
    obsThread = threading.Thread(target=lambda: observe(conf), daemon=True)
    obsThread.start()
    t = threading.Thread(target=lambda: keyboard.wait(), daemon=True)
    t.start()
    ui.startUI()

if __name__ == "__main__":
    main()


