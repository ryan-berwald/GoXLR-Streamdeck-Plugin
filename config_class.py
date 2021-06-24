import keyboard
import toml
import sys

class config:
    def __init__(self, _path, _keyPressFunc):
        self.path = _path
        self.rawfile = []
        self.configFile = None
        self.profiles = []
        self.hotkeyFunc = _keyPressFunc
        self.keys = []
        try:
            self.loadConfig()
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
    def loadConfig(self):
        self.configFile = toml.load(self.path)
        self.rawfile = self.configFile["Hotkeys"]
        print(self.rawfile)
        self.keys = self.rawfile["keys"]
        self.profiles = self.rawfile["profiles"]
        
        for x in range(len(self.keys)):
            keyboard.add_hotkey(self.keys[x], lambda: self.hotkeyFunc(self.profiles[x])) #<-- attach the function to hot-key
            
        
    