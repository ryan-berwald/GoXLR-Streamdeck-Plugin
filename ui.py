from PyQt5 import QtGui
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *
from keyboard import release 
from os import system
class userInterface:
    def __init__(self, goxlrPath):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        
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
        showInterface.triggered.connect(self.showUI)
        self.menu.addAction(showInterface)
        self.menu.addAction(quit)
        self.tray.setContextMenu(self.menu)

        self.window = QWidget()
        layout = QGridLayout()

        #Status check boxes
        vbox = QVBoxLayout()
        self.WsCB = QCheckBox("WebSocket Running")
        self.WsCB.setEnabled(False)
        self.GoXLRCB = QCheckBox("GoXLR Connection")
        self.GoXLRCB.setEnabled(False)
        GroupBox = QGroupBox("Connection Status")
        vbox.addWidget(self.WsCB)
        vbox.addWidget(self.GoXLRCB)
        GroupBox.setLayout(vbox)
        layout.addWidget(GroupBox,0, 0)

        #Config Button
        confButton = QPushButton('Edit Config')
        confButton.clicked.connect(lambda: system(goxlrPath + "config.toml"))
        layout.addWidget(confButton,0,1)


        self.window.setLayout(layout)
        self.window.setWindowTitle("Hotkeys")
        self.app.exec()

    def showUI(self):
        self.window.show()

    def sysTrayClick(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showUI()

