from commandresponse import CommandResponse
from enums.commandenumerations import eCommandType, eCommandAction, eCommandSearchType

class Command(object):
    """A Command is an object that contains instructions to execute
    based on the parameters supplied."""

    def __init__(self):
        self.Name = ""
        self.Aliases = []
        self.Path = ""
        self.HasExecuted = False
        self.Response = CommandResponse()
        self.CommandType = eCommandType.LUNA
        self.CommandAction = eCommandAction.NONE
        self.SearchType = eCommandSearchType.NONE
        self.AssociatedProcess = []
        self.SearchExtension = ""
        self.SearchText = ""

    def fullPath(self):
        lastIndex = self.Path.count() - 1
        if self.Path[lastIndex] != '\\':
            return self.Path + '\\' + self.Filename
        return self.Path + self.Filename


