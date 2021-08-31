from subprocess import Popen
import websocket
import logging
from shutil import which
import threading

class Server:
    def __init__(self) -> None:
        self.serverStarted = False
        self.goXLRConnected = False
        self.clientConnected = False
        self.serverThread = threading.Thread(target=self.startServer, daemon=True)


    def startServer(self) -> None:
        try:
            process = Popen([which("node"), './goxlr.js'])
            if process.poll() == None:
                self.serverStarted = True
        except Exception as e:
            print(e)

    def verifyConnection(self) -> None:
        try:
            websocket.WebSocket().connect("ws://localhost:6805/client")    
            self.clientConnected = True
        except ConnectionRefusedError as e:
            logging.getLogger.error(e)