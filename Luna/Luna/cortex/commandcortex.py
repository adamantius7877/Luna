from command import Command
from enums.commandenumerations import eCommandType, eCommandAction, eCommandSearchType
import json, constants

class CommandCortex:
    """This is the cortex that controls processing and interpreting commands"""

    def __init__(self):
        self.__RefreshCommandActions()

    def InterpretCommand(self, textToInterpret):
        modifiedInput = self.ProcessText(textToInterpret)
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
                    command.CommandType = eCommandType.SEARCH
                    command.SearchText = modifiedInput
                    command.Path = constants.HOME_DIRECTORY
                else:
                    command.CommandType = eCommandType.APPLICATION
                break

        # Strip the rest of the string to get a clear understanding of the rest of the input
        return command

    def ProcessText(self, textToProcess):
        textObject = json.loads(textToProcess)
        text = textObject["text"]
        return text.lower()

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
        self.CommandActionSwitch["search for"] = [eCommandAction.SEARCH]
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
                "search for",
                ]
