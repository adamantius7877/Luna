from command import Command
from cortex.commandcortex import CommandCortex
from cortex.directorycortex import DirectoryCortex
from cortex.applicationcortex import ApplicationCortex
from enums.commandenumerations import eCommandType, eCommandAction, eCommandSearchType
import threading, queue

class Brain(object):
    """description of class"""
    def __init__(self, luna):
        self.CommandActions = []
        self.Luna = luna
        self.CommandCortex = CommandCortex()
        self.DirectoryCortex = DirectoryCortex()
        self.ApplicationCortex = ApplicationCortex()
        self.CommandQueue = queue.Queue()
        self.CommandThread = threading.Thread(target=self.commandQueueWorker, daemon=True)

    def InterpretCommand(self, textToInterpret):
        command = self.CommandCortex.InterpretCommand(textToInterpret)
        if command is None:
            return
        if command.CommandAction != eCommandAction.NONE:
            self.ProcessCommand(command)

    def ProcessCommand(self, command):
        self.CommandQueue.put(command)
        if not self.CommandThread.isAlive():
            self.CommandThread = threading.Thread(target=self.commandQueueWorker, daemon=True)
            self.CommandThread.start()

    def commandQueueWorker(self):
        while True:
            command = self.CommandQueue.get()
            if command:
                self.RunCommand(command)

    def RunCommand(self, command):
        if command.CommandType == eCommandType.LUNA:
            self.RunLunaCommand(command)
        elif command.CommandType == eCommandType.APPLICATION:
            self.RunApplicationCommand(command)
        elif command.CommandType == eCommandType.SEARCH:
            self.RunSearchCommand(command)

    def RunLunaCommand(self, command):
        return

    def RunApplicationCommand(self, command):
        if command.CommandAction == eCommandAction.OPEN:
            self.Luna.Speak("Opening " + command.Name)
            self.ApplicationCortex.RunCommand(command)
        elif command.CommandAction == eCommandAction.CLOSE:
            self.ApplicationCortex.StopCommand(command)

    def RunSearchCommand(self, command):
        self.Luna.Speak("Searching")
        self.DirectoryCortex.SearchFiles(command);
        self.Luna.Speak("Search complete.  I found " + str(len(command.Response.Results)) + " files containing the text " + command.SearchText)
