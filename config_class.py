import FileObserver
import logging
from keyboard import add_hotkey
import toml
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler 

class config:
    def __init__(self, keyPressFunc, path, goxlrdir, server):
        self.path = path
        self.rawfile = []
        self.configFile = None
        self.profiles = []
        self.hotkeyFunc = keyPressFunc
        self.keys = []
        self.server = server
        self.loadConfig(goxlrdir)
        logging.getLogger().info(f"\n\tPath: {self.path}\n\tProfiles: {self.profiles}\n\tKeys: {self.keys}")

    def loadConfig(self, goXlrDir):
        try:
            self.configFile = toml.load(self.path)
        except FileNotFoundError as e:
            logging.getLogger().error("Config file not found, creating sample now")
            with open(goXlrDir + 'config.toml', 'w') as file:
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
""")
        finally:
            self.rawfile = self.configFile["Hotkeys"]
            print(self.rawfile)
            self.keys = self.rawfile["keys"]
            self.profiles = self.rawfile["profiles"]
            print(self.keys)
            print(self.profiles)
            for x in range(len(self.keys)):
                add_hotkey(self.keys[x], self.hotkeyFunc, args=(self.profiles[x], self.keys[x], self.server)) #<-- attach the function to hot-key    


