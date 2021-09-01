from subprocess import Popen
import websocket
import logging
from shutil import which
import threading
import json

class Server:
    def __init__(self) -> None:
        self.serverStarted = False
        self.goXLRConnected = False
        self.clientConnected = False
        self.serverThread = threading.Thread(target=self.startServer, daemon=True)


    def startServer(self, ui) -> None:
        try:
            process = Popen([which("node"), './goxlr.js'])
            if process.poll() == None:
                self.serverStarted = True
        except Exception as e:
            print(e)

    def verifyConnection(self, ui) -> None:
        try:
            ws = websocket.WebSocket()
            ws.connect("ws://localhost:6805/client")
            ws.send('verifyconnection=')
            message = json.loads(ws.recv())
            print(message["Client"])
            ui.WsLabel.setText(ui.CHECKMARK + " WebSocket Status")  
        except ConnectionRefusedError as e:
            logging.getLogger.error(e)
