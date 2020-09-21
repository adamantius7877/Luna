from command import Command
from cortex.commandcortex import CommandCortex
from cortex.directorycortex import DirectoryCortex
from enums.commandenumerations import eCommandType, eCommandAction, eCommandSearchType
import threading, queue

class Brain(object):
    """description of class"""
    def __init__(self, luna):
        self.CommandActions = []
        self.Luna = luna
        self.__RefreshCommandActions()
        self.CommandCortex = CommandCortex()
        self.DirectoryCortex = DirectoryCortex()
        self.CommandQueue = queue.Queue()
        self.CommandThread = threading.Thread(target=self.commandQueueWorker, daemon=True)

    def InterpretCommand(self, textToInterpret):
        command = self.CommandCortex.InterpretCommand(textToInterpret)
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

    def __RefreshCommandActions(self):
        self.CommandActionSwitch = dict()
        self.CommandActionSwitch["open"] = [eCommandAction.OPEN]
        self.CommandActionSwitch["add"] = [eCommandAction.OPEN]
        self.CommandActionSwitch["close"] = [eCommandAction.CLOSE]
        self.CommandActionSwitch["create"] = [eCommandAction.CREATE]
        self.CommandActionSwitch["pause"] = [eCommandAction.PAUSE]
        self.CommandActionSwitch["play"] = [eCommandAction.PLAY]
        self.CommandActionSwitch["unlock"] = [eCommandAction.UNLOCK]
        self.CommandActionSwitch["search online for"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search online"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search network for"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search network"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search directories for"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search directories"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search files for"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search files"] = [eCommandAction.SEARCH]
        self.CommandActions = [
                "open",
                "add",
                "close",
                "create",
                "pause",
                "play",
                "unlock",
                "search online for",
                "search online",
                "search network for",
                "search network",
                "search directories for",
                "search directories",
                "search files for",
                "search files",
                ]
        self.CommandActionSwitch

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
            self.ApplicationCortex.RunCommand(command)
        elif command.CommandAction == eCommandAction.CLOSE:
            self.ApplicationCortex.StopCommand(command)
        elif command.CommandAction == eCommandAction.CREATE:
            self.ApplicationCortex.StopCommand(command)

    def RunSearchCommand(self, command):
        self.Luna.Speak("Searching")
        self.DirectoryCortex.SearchFiles(command);
        self.Luna.Speak("Search complete.  I found " + str(len(command.Response.Results)) + " files containing the text " + command.SearchText)
