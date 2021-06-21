from typing import AnyStr
from PySide6.QtUiTools import QUiLoader
import keyboard
import websocket



def keyPress():
    ws = websocket.WebSocket()
    ws.connect("ws://localhost:6805/client")
    ws.send("changeprofile=Desk")
    print(ws.recv())
    ws.close()

requestedProf = "Gaming"
shortcut = 'F13' #define your hot-key
print('Hotkey set as:', shortcut)

keyboard.add_hotkey(shortcut, keyPress) #<-- attach the function to hot-key

print("Press ESC to stop.")
keyboard.wait('esc')
