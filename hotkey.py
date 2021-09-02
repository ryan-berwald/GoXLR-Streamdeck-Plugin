from time import sleep
import keyboard
import websocket

import threading
import logging
from subprocess import Popen, PIPE
from config_class import config
from sys import exit as ex
from os import mkdir, path
from pathlib import Path, WindowsPath
from ui import userInterface
from Server import Server

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
    try:
        ui = userInterface(goXlrDir)
        """ obsThread = threading.Thread(target=observe, daemon=True)
        obsThread.start() """
        server = Server(ui)
        logger.info("Listening for hotkeys...")
        conf = config(keyPress, goXlrDir + "\\config.toml", goXlrDir, server)
        t = threading.Thread(target=lambda: keyboard.wait(), daemon=True)
        t.start()
        ui.startUI()

    except KeyboardInterrupt as e:
        logger.error(e)       
    finally:
        ex("exiting")    

if __name__ == "__main__":
    main()


