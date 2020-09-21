from commandresponse import CommandResponse
from enums.commandenumerations import eCommandType, eCommandAction, eCommandSearchType

class Command(object):
    """A Command is an object that contains instructions to execute
    based on the parameters supplied."""

    def __init__(self):
        self.Name = ""
        self.FileName = ""
        self.Aliases = []
        self.Arguments = "" 
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
        lastIndex = len(self.Path) - 1
        if self.Path[lastIndex] != '\\':
            return self.Path + '\\' + self.FileName
        return self.Path + self.FileName


