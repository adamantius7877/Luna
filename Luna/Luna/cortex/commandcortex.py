from command import Command
from enums.commandenumerations import eCommandType, eCommandAction, eCommandSearchType
import json, constants

class CommandCortex:
    """This is the cortex that controls processing and interpreting commands"""

    def __init__(self):
        self.DefaultCommands = []
        self.__RefreshCommandActions()
        self.__GetDefaultComands()

    def InterpretCommand(self, textToInterpret):
        modifiedInput = self.ProcessText(textToInterpret)
        if len(modifiedInput) == 0: return
        command = Command()
        indexOfCommandAction = -1

        # First make sure that this was even meant for luna and remove the name if so
        indexOfName = modifiedInput.find(constants.LUNA_NAME)
        if indexOfName == -1:
            return command
        modifiedInput = modifiedInput.replace(constants.LUNA_NAME, constants.EMPTY_STRING)

        # Next determine the action associated with the command
        # For now this will also include determining command type
        for commandAction in self.CommandActions:
            indexOfCommandAction = modifiedInput.find(commandAction)
            if indexOfCommandAction >= 0:
                modifiedInput = modifiedInput.replace(commandAction, constants.EMPTY_STRING)
                modifiedInput = modifiedInput.strip()
                command.CommandAction = self.CommandActionSwitch[commandAction][0]
                if command.CommandAction == eCommandAction.SEARCH:
                    if commandAction.find("online") >= 0:
                        command = self.__GetCommand("chrome")
                        command.Arguments = constants.GOOGLE_QUERY_BASE + modifiedInput
                    else:
                        command.CommandType = eCommandType.SEARCH
                        command.SearchText = modifiedInput
                        command.Path = constants.HOME_DIRECTORY
                    break
                    #return command
                elif command.CommandAction == eCommandAction.FOCUS or\
                     command.CommandAction == eCommandAction.PAUSE or\
                     command.CommandAction == eCommandAction.PLAY:
                    command.CommandType = eCommandType.LUNA
                    command.Name = modifiedInput
                    break
                    #return command
                else:
                    command = self.__GetCommand(modifiedInput)
                    #return command
                    break
                break

        return command

    def ProcessText(self, textToProcess):
        if textToProcess.find('{') < 0:
            return textToProcess;
        textObject = json.loads(textToProcess)
        text = textObject["text"]
        if len(text) > 0:
            print(text)
        return text.lower()

    def __GetCommand(self, possibleName):
        for command in self.DefaultCommands:
            if command.Name == possibleName:
                return self.GetCopy(command)
            else:
                for alias in command.Aliases:
                    if alias == possibleName:
                        return command

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
        self.CommandActionSwitch["search on line for"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search online"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search on line"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search network for"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search network"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search directories for"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search directories"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search for"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search files for"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["search files"] = [eCommandAction.SEARCH]
        self.CommandActionSwitch["switch to"] = [eCommandAction.FOCUS]
        self.CommandActionSwitch["switched to"] = [eCommandAction.FOCUS]
        self.CommandActionSwitch["focus"] = [eCommandAction.FOCUS]
        self.CommandActionSwitch["switch focus to"] = [eCommandAction.FOCUS]
        self.CommandActionSwitch["switched focus to"] = [eCommandAction.FOCUS]
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
                "search for",
                "switch to"
                ]

    def __GetDefaultComands(self):
        command = Command()
        command.Name = "chrome"
        command.Aliases.append("internet")
        command.Aliases.append("online")
        command.Aliases.append("on line")
        command.FileName = "chrome.exe"
        command.Path = "C:\\Program Files (x86)\\Google\\Chrome\\Application"
        command.CommandType = eCommandType.APPLICATION
        command.CommandAction = eCommandAction.OPEN
        self.DefaultCommands.append(command)
        command = Command()
        command.Name = "avengers"
        command.Aliases.append("marvel avengers")
        command.FileName = "Marvel's Avengers.url"
        command.Path = "C:\\Users\\adama\\OneDrive\\Desktop"
        command.CommandType = eCommandType.APPLICATION
        command.CommandAction = eCommandAction.OPEN
        self.DefaultCommands.append(command)
        command = Command()
        command.Name = "vim"
        command.Aliases.append("them")
        command.FileName = "gvim.exe"
        command.Path = "C:\\Program Files (x86)\\Vim\\vim81"
        command.CommandType = eCommandType.APPLICATION
        command.CommandAction = eCommandAction.OPEN
        self.DefaultCommands.append(command)
        command.Name = "input"
        command.Aliases.append("in put")
        command.FileName = ""
        command.Path = ""
        command.CommandType = eCommandType.LUNA
        command.CommandAction = eCommandAction.OPEN
        self.DefaultCommands.append(command)

    def GetCopy(self, command):
        commandCopy = Command()
        commandCopy.Name = command.Name
        commandCopy.FileName = command.FileName
        commandCopy.Arguments = command.Arguments
        commandCopy.Path = command.Path
        commandCopy.CommandType = command.CommandType
        commandCopy.CommandAction = command.CommandAction
        commandCopy.SearchType = command.SearchType
        commandCopy.SearchExtension = command.SearchExtension
        commandCopy.SearchText = command.SearchText
        return commandCopy
