import logging
import keyboard
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
        
        for x in range(len(self.keys)):
            keyboard.add_hotkey(self.keys[x], lambda: self.hotkeyFunc(self.profiles[x])) #<-- attach the function to hot-key
            
        
    