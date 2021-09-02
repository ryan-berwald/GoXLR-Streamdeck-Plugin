from subprocess import Popen
import websocket 
import logging
from shutil import which
import threading
import json

class Server:
    def __init__(self,ui) -> None:
        self.ui = ui
        self.serverStarted = False
        self._serverThread = threading.Thread(target=self.startServer, daemon=True)
        self._serverThread.start()
        try:
            self.ws = websocket.WebSocketApp("ws://localhost:6805/client", on_message = self.on_message)
            wsThread = threading.Thread(target = self.ws.run_forever)
            wsThread.start()
        except Exception as e:
            print(e)
            logging.getLogger().error(e)
            

    def startServer(self) -> None:
        try:
            process = Popen([which("node"), './goxlr.js'])
            if process.poll() == None:
                self.serverStarted = True
        except Exception as e:
            print(e)

    def updateUI(self, wsStatus, goXLRStatus, serverStatus) -> None:
        if wsStatus == True:
            self.ui.WsLabel.setText(self.ui.CHECKMARK + " Client Connection Status")
        else:
            self.ui.WsLabel.setText(self.ui.CROSSMARK + " Client Connection Status")

        if goXLRStatus == True:
            self.ui.GoXLRLabel.setText(self.ui.CHECKMARK + " GoXLR Connection Status")
        else:
            self.ui.GoXLRLabel.setText(self.ui.CROSSMARK + " GoXLR Connection Status")

        if serverStatus == True:
            self.ui.ServerLabel.setText(self.ui.CHECKMARK + " Server Status")
        else:
            self.ui.ServerLable.setText(self.ui.CROSSMARK + " Server Connection Status")

    
    def on_message(self, ws, message):
        logging.getLogger().info(message)
        self.updateUI(json.loads(message)["Client"], json.loads(message)["GoXLR"], self.serverStarted)
        

    def on_error(ws, error):
        print(error)

    def on_close(ws, close_status_code, close_msg):
        print("### closed ###")
