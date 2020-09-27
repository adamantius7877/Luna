from common.command import Command
from .cortex.commandcortex import CommandCortex
from .cortex.directorycortex import DirectoryCortex
from .cortex.applicationcortex import ApplicationCortex
from .cortex.displaycortex import DisplayCortex
from enums.commandenumerations import eCommandType, eCommandAction, eCommandSearchType
from datetime import datetime
import sys, threading, queue, json, common

if sys.platform == 'cli':
    from serial.serialcli import Serial
else:
    import os
    # chose an implementation, depending on os
    if os.name == 'nt':  # sys.platform == 'win32':
        from .cortex.wincortex import OSCortex
    elif os.name == 'posix':
        from .cortex.nixcortex import OSCortex
    elif os.name == 'java':
        from .cortex.maccortex import OSCortex
    else:
        raise ImportError(
            "Sorry: no implementation for your platform ('{}') available".format(
                os.name
            )
        )

class Brain(object):
    """description of class"""
    def __init__(self, luna):
        self.CommandActions = []
        self.Luna = luna
        self.BaseDirectories = []
        self.CommandCortex = CommandCortex()
        self.DirectoryCortex = DirectoryCortex()
        self.ApplicationCortex = ApplicationCortex()
        self.OSCortex = OSCortex()
        self.ExectuableExtension = self.OSCortex.GetExecutableExtension() 
        self.DisplayCortex = DisplayCortex(self.Luna)
        self.CommandQueue = queue.Queue()
        self.CommandThread = threading.Thread(target=self.commandQueueWorker, daemon=True)
        self.DisplayCortex.DisplayInputWindow()
        threading.Thread(target=self.GetAllApplications, daemon=True).start()

    def GetAllApplications(self):
        self.ExectuableExtension = self.OSCortex.GetExecutableExtension()
        self.BaseDirectories = self.OSCortex.GetDrives()
        generateCommands = True
        try:
            test = common.config.APPLICATION_COMMAND_FILE_PATH
            f = open(test, "r")
            test2 = f.read()
            generateCommands = False
        except Exception:
            print(Exception.args)


        if not generateCommands:
            jsonApplicationCommands = json.loads(test2)
            self.LoadApplicationCommandsFromJsonObject(jsonApplicationCommands)
            if len(self.CommandCortex.AllApplicationCommands) == 0:
                generateCommands = True
            else:
                self.PrintTimeAndMessage("Commands loaded")

        if generateCommands:
            searchCommands = self.CommandCortex.GetExecutableSearchCommandsForPath(self.BaseDirectories, self.ExectuableExtension)
            commands = []

            self.PrintTimeAndMessage("Start Time =")
            for searchCommand in searchCommands:
                self.DirectoryCortex.SearchFiles(searchCommand)
                for result in searchCommand.Response.Results:
                    command = self.CommandCortex.GetCommandForApplicationPath(result)
                    self.CommandCortex.AllApplicationCommands.append(command)
                    commands.append(self.CommandCortex.GetJsonObjectFromApplicationCommand(command))
            self.PrintTimeAndMessage("I found " + str(len(commands)) + " executables across " + str(len(self.BaseDirectories)) + " directories: ")
            commandsJsonString = json.dumps(commands, indent=4)
            self.PrintTimeAndMessage("Writing to file now: ")
            f = open(common.config.APPLICATION_COMMAND_FILE_PATH, "a")
            f.write(commandsJsonString)
            f.close()
            self.PrintTimeAndMessage("Finished writing to file now: ")

    def LoadApplicationCommandsFromJsonObject(self, jsonApplicationCommands):
        for jsonCommand in jsonApplicationCommands:
            self.CommandCortex.AllApplicationCommands.append(self.CommandCortex.GetApplicationCommandFromJsonObject(jsonCommand))

    def PrintTimeAndMessage(self, message):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(message, current_time)

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
                threading.Thread(target=self.RunCommand, args=[command],daemon=True).start()

    def RunCommand(self, command):
        if command.CommandType == eCommandType.LUNA:
            self.RunLunaCommand(command)
        elif command.CommandType == eCommandType.APPLICATION:
            self.RunApplicationCommand(command)
        elif command.CommandType == eCommandType.SEARCH:
            self.RunSearchCommand(command)

    def RunLunaCommand(self, command):
        if command.CommandAction == eCommandAction.OPEN and command.Name == "input":
            self.DisplayCortex.DisplayInputWindow()
        elif command.CommandAction == eCommandAction.FOCUS:
            self.OSCortex.SwitchActiveWindow(command)
        elif command.CommandAction == eCommandAction.MUTE:
            self.OSCortex.Mute()
        elif command.CommandAction == eCommandAction.UNMUTE:
            self.OSCortex.Unmute()
        elif command.CommandAction == eCommandAction.PLAY or command.CommandAction == eCommandAction.PAUSE:
            self.OSCortex.TogglePlayPause()

    def RunApplicationCommand(self, command):
        if command.CommandAction == eCommandAction.OPEN:
            self.Luna.Speak("Opening " + command.Name)
            self.ApplicationCortex.RunCommand(command)
        elif command.CommandAction == eCommandAction.CLOSE:
            self.ApplicationCortex.StopCommand(command)

    def RunSearchCommand(self, command):
        if command.SearchType == eCommandSearchType.ONLINE:
            self.ApplicationCortex.RunCommand(command)
        else:
            self.Luna.Speak("Searching")
            self.DirectoryCortex.SearchFiles(command);
            self.Luna.Speak("Search complete.  I found " + str(len(command.Response.Results)) + " files containing the text " + command.SearchText)
            self.DisplayCortex.DisplayResult(command)
