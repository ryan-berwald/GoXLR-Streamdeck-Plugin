# Import the required libraries
import tkinter as tk
from pystray import MenuItem as item
import pystray
from PIL import Image, ImageTk
from os import system


class ui:
    CHECKMARK = "\u2705"
    CROSSMARK = "\u274c"
    def __init__(self, goXlrDir) -> None:
        self.goXlrDir = goXlrDir

        # Create an instance of tkinter frame or self.window
        self.win=tk.Tk()

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
        self.frm_Buttons = tk.Frame()
        self.btn_EditConfig = tk.Button(text="Edit Config", master=self.frm_Buttons, command=lambda: system(goXlrDir + "config.toml"))
        self.btn_EditConfig.pack()
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

    