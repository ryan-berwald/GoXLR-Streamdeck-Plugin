import websocket

import threading
import logging
from subprocess import Popen, PIPE
from config_class import config
from sys import exit as ex
from os import mkdir, path
from pathlib import Path
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
    
def main():
    try:
        ui = userInterface(goXlrDir)
        """ obsThread = threading.Thread(target=observe, daemon=True)
        obsThread.start() """
        server = Server()
        server.startServer(ui)
        logger.info("Listening for hotkeys...")
        connThread = threading.Thread(target=server.verifyConnection, daemon=True, args={ui})
        connThread.start()
        ui.startUI()

    except KeyboardInterrupt as e:
        logger.error(e)       
    finally:
        ex("exiting")    

if __name__ == "__main__":
    main()


