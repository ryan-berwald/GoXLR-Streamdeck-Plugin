import keyboard
import threading
import logging
from config_class import config
from os import mkdir, path
import os
from pathlib import Path
import uiTKinter
from Server import Server
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import atexit

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
    logger.info(f'hotkey pressed {profile}; {keys}')
    try:
        server.ws.send(f'changeprofile={profile}')
    except Exception as e:
        logger.error(e)

def main():     
    conf = config(keyPress, goXlrDir)
    ui = uiTKinter.ui(goXlrDir, conf)
    server = Server(ui)
    for x in range(len(conf.keys)):
        keyboard.add_hotkey(conf.keys[x], conf.hotkeyFunc, args=(conf.profiles[x], conf.keys[x], server)) #<-- attach the function to hot-key
    
    logger.info(f"\n\tPath: {conf.configFilePath}\n\tProfiles: {conf.profiles}\n\tKeys: {conf.keys}")
    class Event(FileSystemEventHandler):
        def dispatch(self, event):
            if event.src_path == goXlrDir + "config.toml" and event.event_type == "modified": 
                conf.loadConfig(goXlrDir)
    def observe(conf):
        event_handler = Event()
        observer = Observer()
        observer.schedule(event_handler, goXlrDir, recursive=True)
        observer.start()
    obsThread = threading.Thread(target=lambda: observe(conf), daemon=True)
    obsThread.start()
    logger.info("Listening for hotkeys...")
    t = threading.Thread(target=lambda: keyboard.wait(), daemon=True)
    t.start()
    atexit.register(conf.save_Config)
    ui.startLoop()

    server.ws.close()
    
if __name__ == "__main__":
    main()


