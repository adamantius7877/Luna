from commandresponse import CommandResponse
import os
class DirectoryCortex:
    """This cortex handles any File IO with the OS as well as searches"""

    def SearchFiles(self, command):
        checkExtension = len(command.SearchExtension) > 0
        command.Response = SearchResponse()
        for root, dirs, files in os.walk(command.Path):
            for file in files:
                hasSearch = file.lower().find(command.SearchText)
                if checkExtension and hasSearch:
                    hasSearch = file.endswith(command.SearchExtension)
                if hasSearch >= 0:
                    searchResult = FileSearchResult()
                    searchResult.FileName = file
                    searchResult.FileDirectory = dirs
                    searchResult.FilePath = os.path.join(root,file)
                    command.Response.Results.append(searchResult)

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