import logging
from typing import Any
import toml
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler 
from pathlib import Path
class config:
    def __init__(self, keyPressFunc, goxlrdir):
        self.configFilePath = Path(goxlrdir + "config.toml")
        self.rawfile = self.loadConfig()
        self.profiles = self.rawfile["Hotkeys"]["profiles"]
        self.hotkeyFunc = keyPressFunc
        self.keys = self.rawfile["Hotkeys"]["keys"]
        self.installDir = self.rawfile["InstallDirectory"]["FullPath"]
        self.start_with_windows = self.rawfile["StartSettings"]["startwithwindows"]

    def loadConfig(self):
        if not Path.is_file(Path(self.configFilePath)):
            logging.getLogger().error("Config file not found, creating sample now")
            with open(self.configFilePath, 'w') as file:
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

[InstallDirectory]
FullPath="C:\\\Program Files (x86)\\\TC-Helicon\\\GOXLR"

[StartSettings]
startwithwindows=false

""")
        with open(self.configFilePath, "r") as f:
            return toml.load(f)

    def save_Config(self):
        self.rawfile["Hotkeys"]["keys"] = self.keys
        self.rawfile["Hotkeys"]["profiles"] = self.profiles
        self.rawfile["StartSettings"]["startwithwindows"] = self.start_with_windows
        with open(self.configFilePath, "w") as f:
            toml.dump(self.rawfile, f)
            f.close()