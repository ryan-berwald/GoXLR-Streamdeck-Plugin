import logging
from keyboard import add_hotkey
import toml
import logging

class config:
    def __init__(self, _keyPressFunc, _path):
        self.path = _path
        self.rawfile = []
        self.configFile = None
        self.profiles = []
        self.hotkeyFunc = _keyPressFunc
        self.keys = []
        self.loadConfig()
        logging.getLogger().info(f"\n\tPath: {self.path}\n\tProfiles: {self.profiles}\n\tKeys: {self.keys}")

    def loadConfig(self):
        try:
            self.configFile = toml.load(self.path)
        except FileNotFoundError as e:
            logging.getLogger().error(e)
            raise e
        self.rawfile = self.configFile["Hotkeys"]
        print(self.rawfile)
        self.keys = self.rawfile["keys"]
        self.profiles = self.rawfile["profiles"]
        print(self.keys)
        print(self.profiles)
        for x in range(len(self.keys)):
            add_hotkey(self.keys[x], self.hotkeyFunc, args=(self.profiles[x], self.keys[x])) #<-- attach the function to hot-key    