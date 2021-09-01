from PyQt5 import QtGui
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from keyboard import release 
from os import stat, system
class userInterface:
    CHECKMARK = "\u2705"
    CROSSMARK = "\u274c"
    def __init__(self, goxlrPath):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.window = QWidget()
        # Adding an icon
        icon = QIcon("./Assets/icon.ico")
        
        # Adding item on the menu bar
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(icon)
        self.tray.setVisible(True)
        self.tray.activated.connect(self.sysTrayClick)

        # Creating the options
        self.menu = QMenu()
        quit = QAction("Quit")
        quit.triggered.connect(self.app.quit)
        showInterface = QAction("Show UI")
        showInterface.triggered.connect(self.window.show)

        self.menu.addAction(showInterface)
        self.menu.addAction(quit)
        self.tray.setContextMenu(self.menu)

        layout = QGridLayout()

        #Status check boxes
        vbox = QVBoxLayout()
        self.WsLabel = QLabel(self.CROSSMARK + " WebSocket Status")
        self.GoXLRLabel = QLabel(self.CROSSMARK + " GoXLR Status")
        self.ServerLabel = QLabel(self.CROSSMARK + " Server Status")
        GroupBox = QGroupBox("Connection Status")
        vbox.addWidget(self.WsLabel)
        vbox.addWidget(self.GoXLRLabel)
        vbox.addWidget(self.ServerLabel)
        GroupBox.setLayout(vbox)
        layout.addWidget(GroupBox,0, 0)

        #Config Button
        confButton = QPushButton('Edit Config')
        confButton.clicked.connect(lambda: system(goxlrPath + "config.toml"))
        layout.addWidget(confButton,0,1)


        self.window.setLayout(layout)
        self.window.setWindowTitle("Hotkeys")       

    def sysTrayClick(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.window.show()
    
    def startUI(self):
        self.app.exec()
