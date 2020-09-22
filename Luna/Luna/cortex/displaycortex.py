import tkinter as tk
from command import Command
from enums.commandenumerations import eCommandType, eCommandAction, eCommandSearchType
import threading

class DisplayCortex():
    """This cortex handles displaying UI elements"""

    def __init__(self, luna):
        self.window = []
        self.commands = []
        self.InputWindow = []
        self.Luna = luna

    def DisplayResult(self, command):
        if command.CommandAction == eCommandAction.SEARCH:
            lock = threading.Lock()
            lock.acquire()
            window = tk.Tk()
            for searchResult in command.Response.Results:
                results = tk.Label(master=window, text=searchResult.FileName, foreground="white", background="black")
                results.pack()
            window.mainloop()
            lock.release()

    def RunCommand(self, event):
        commandToRun = event.widget.get()
        self.Luna.InterpretCommand(commandToRun)

    def TryDisplay(self):
        window = tk.Tk()
        label = tk.Label(text="Command:")
        label.pack()
        entry = tk.Entry()
        entry.bind("<Return>", self.RunCommand)
        entry.pack()
        #button = tk.Button(text="Run Command")
        #button.pack()
        window.mainloop()


    def DisplayInputWindow(self):
        threading.Thread(target=self.TryDisplay, daemon=True).start()
