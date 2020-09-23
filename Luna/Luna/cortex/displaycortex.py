import tkinter as tk
from command import Command
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
            window.title('Luna Search Results')
            window.minsize(300,200)
            print("---Begin Search Results---")
            for searchResult in command.Response.Results:
                print(searchResult.FileName)
                print(" - " + searchResult.FilePath)
                results = tk.Label(master=window, text=searchResult.FileName, foreground="white", background="black")
                results.pack()
            print("---End  Search  Results---")
            window.bell()
            window.mainloop()
            lock.release()

    def RunCommand(self, event):
        commandToRun = event.widget.get()
        self.Luna.InterpretCommand(commandToRun)

    def RunSpeak(self, event):
        textToSpeak = event.widget.get()
        self.Luna.Speak(textToSpeak)

    def DisplayThread(self):
        window = tk.Tk()
        window.title('Luna Input Test Window')
        window.minsize(300,200)
        label = tk.Label(text="Command:")
        label.pack()
        entry = tk.Entry(width=45)
        entry.bind("<Return>", self.RunCommand)
        entry.pack()
        label = tk.Label(text="Speak:")
        label.pack()
        entry = tk.Entry(width=45)
        entry.bind("<Return>", self.RunSpeak)
        entry.pack()
        #button = tk.Button(text="Run Command")
        #button.pack()
        window.mainloop()


    def DisplayInputWindow(self):
        threading.Thread(target=self.DisplayThread, daemon=True).start()
