# Import the required libraries
from sys import getwindowsversion
import tkinter as tk
from tkinter import filedialog, IntVar
from pathlib import Path
from pystray import MenuItem as item
import pystray
import pystray._win32
from PIL import Image
from os import system, getcwd, remove
import win32com.client

class ui:
    CHECKMARK = "\u2705"
    CROSSMARK = "\u274c"
    def __init__(self, goXlrDir, conf) -> None:
        self.goXlrDir = goXlrDir
        self.exeDir = ""
        # Create an instance of tkinter frame or self.window
        self.win=tk.Tk()
        self.conf = conf
        # Setting text vars
        self.clientStatus = tk.StringVar(value=self.CROSSMARK + " Client Connection Status")
        self.goXLRStatus = tk.StringVar(value=self.CROSSMARK + " GoXLR Connection Status")
        self.serverStatus = tk.StringVar(value=self.CROSSMARK + " Server Connection Status")

        #Creating frame and packing labels
        self.frm_Status = tk.Frame()
        self.lbl_Client = tk.Label(textvariable=self.clientStatus, master=self.frm_Status)
        self.lbl_GoXLR = tk.Label(textvariable=self.goXLRStatus, master=self.frm_Status)
        self.lbl_Server = tk.Label(textvariable=self.serverStatus, master=self.frm_Status)
        self.lbl_Server.pack()
        self.lbl_GoXLR.pack()
        self.lbl_Client.pack()
        self.frm_Status.pack()

        #Creating frame and packing buttons
        self.cb = IntVar()
        self.frm_Buttons = tk.Frame()
        self.btn_EditConfig = tk.Button(text="Edit Config", master=self.frm_Buttons, command=lambda: system(goXlrDir + "config.toml"))
        self.chk_StartWindows = tk.Checkbutton(text="Start with Windows", master=self.frm_Buttons, command=self.start_with_windows, variable=self.cb, onvalue=1, offvalue=0 )
        
        if self.conf.start_with_windows:
            self.chk_StartWindows.select()
        
        self.btn_EditConfig.pack()
        self.chk_StartWindows.pack()
        self.frm_Buttons.pack()
        self.win.title("Streamdeck GoXLR Emulator")

        self.win.protocol('WM_DELETE_WINDOW', self.hide_window)

    def startLoop(self):
        self.win.mainloop()

    # Define a function for quit the self.window
    def quit_window(self, icon, item):
        icon.stop()
        self.win.destroy()

    # Define a function to show the self.window again
    def show_window(self, icon, item):
        icon.stop()
        self.win.after(0,self.win.deiconify())

    # Hide the self.window and show on the system taskbar
    def hide_window(self):
        self.win.withdraw()
        image=Image.open("./Assets/icon.ico")
        menu=(item('Show UI', self.show_window), item('Quit', self.quit_window))
        icon=pystray.Icon("name", image, "My System Tray Icon", menu)
        icon.run()

    def start_with_windows(self):
        if self.cb.get() == 1:
            try:
                ws = win32com.client.Dispatch("wscript.shell")
                exe_Shortcut = ws.CreateShortCut(f"{Path.home()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\GoXLRApp.lnk")
                server_Shortcut = ws.CreateShortCut(f"{Path.home()}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\GoXLRHotkey.lnk")

                if Path.is_file(Path("C:\\Program Files (x86)\\TC-Helicon\\GOXLR\\GoXLR App.exe")):
                    exe_Shortcut.TargetPath = "C:\\Program Files (x86)\\TC-Helicon\\GOXLR\\Go XLR App.exe"
                else:
                    exe_Shortcut.TargetPath = filedialog.askopenfile(initialdir="C:\\Program Files (x86)\\TC-Helicon\\GOXLR\\",initialfile="Go XLR App.exe")

                server_Shortcut.TargetPath = f"{getcwd()}\\hotkey.exe"
                exe_Shortcut.Save()
                server_Shortcut.Save()
                self.conf.start_with_windows = True
            except Exception as exception:
                print(exception)
        elif self.cb.get() == 0:
            try:
                remove("C:\\Users\\rberw\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\GoXLRApp.lnk")
            except FileNotFoundError as e:
                pass
            finally:
                self.conf.start_with_windows = False
        