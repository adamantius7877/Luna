from common.commandresponse import CommandResponse
import os
class DirectoryCortex:
    """This cortex handles any File IO with the OS as well as searches"""

    def SearchFiles(self, command):
        checkExtension = len(command.SearchExtension) > 0
        command.Response = SearchResponse()
        for root, dirs, files in os.walk(command.Path):
            for file in files:
                hasSearch = False
                if command.SearchText == "*":
                    hasSearch = True
                else:
                    hasSearch = file.lower().find(command.SearchText) >= 0
                if checkExtension and hasSearch:
                    hasSearch = file.endswith(command.SearchExtension)
                if hasSearch:
                    if self.HasSpecialCharacters(file):
                        continue
                    searchResult = FileSearchResult()
                    searchResult.FileName = file
                    fullPath = os.path.join(root, file)
                    searchResult.FileDirectory = os.path.dirname(fullPath)
                    searchResult.FilePath = fullPath
                    command.Response.Results.append(searchResult)

    def HasSpecialCharacters(self, file):
        specialCharacters = ["$"]
        for specialCharacter in specialCharacters:
            if file.find(specialCharacter) >= 0:
                return True
        return False

class SearchResponse(CommandResponse):
    """The response given when executing a search command"""

    def __init__(self):
        self.Results = []

class FileSearchResult():
    """A model of a single result found while searching files"""

    def __init__(self):
        self.FileName = ""
        self.FileDirectory = ""
        self.FilePath = ""