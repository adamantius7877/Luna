from ..neurons.centralnerve import CentralNerve
from ...common import constants
from ...common.application import Application

import uuid, os

class OSCortex(object):
    '''This is the base cortex used as an abstract class for all operating system cortex modules'''

    def __init__(self, lobe):
        self.Lobe = lobe
        self.AllApplications = []
        self.AvailableApplications = []
        self.GetApplications()
        self.CentralNerve = CentralNerve(self.Lobe)
        self.CentralNerve.AcceptAll = True

    def __enter__(self):
        return self

    def __exit__(self,*_):
        pass

    def CheckCentralNerveData(self, data):
        if data[0] == constants.GET_ALL_APPLICATIONS_NERVE_MESSAGE:
            print('Getting Applications')
            applications = []
            for application in self.AvailableApplications:
                applications.append([application.Name, application.ID, application.Path])

            self.CentralNerve.Stimulate(applications)

    def Activate(self):
        self.CentralNerve.Activate(self.CheckCentralNerveData)

    def Deactivate(self):
        self.CentralNerve.Deactivate()

    def GetApplications(self):
        possibleapps = ['vim','firefox','chromium']
        searchResponse = self.SearchFiles('','/usr/bin','*')
        for result in searchResponse.Results:
            application = Application()
            application.ID = uuid.uuid4().hex
            application.Name = result.FileName
            application.Path = result.FileDirectory
            application.Keywords.append(application.Name)
            self.AllApplications.append(application)
            self.AvailableApplications.append(application)
            #if application.Name in possibleapps:
            #    self.AvailableApplications.append(application)

    def SearchFiles(self, extension, path, searchText):
        response = SearchResponse()

        checkExtension = len(extension) > 0
        response = SearchResponse()
        for root, dirs, files in os.walk(path):
            for file in files:
                hasSearch = False
                if searchText == "*":
                    hasSearch = True
                else:
                    hasSearch = file.lower().find(searchText) >= 0
                if checkExtension and hasSearch:
                    hasSearch = file.endswith(extension)
                if hasSearch:
                    if self.HasSpecialCharacters(file):
                        continue
                    searchResult = FileSearchResult()
                    searchResult.FileName = file
                    fullPath = os.path.join(root, file)
                    searchResult.FileDirectory = os.path.dirname(fullPath)
                    searchResult.FilePath = fullPath
                    response.Results.append(searchResult)
        return response

    def HasSpecialCharacters(self, file):
        specialCharacters = ["$"]
        for specialCharacter in specialCharacters:
            if file.find(specialCharacter) >= 0:
                return True
        return False



class SearchResponse(object):
    """The response given when executing a search command"""

    def __init__(self):
        self.Results = []

class FileSearchResult():
    """A model of a single result found while searching files"""

    def __init__(self):
        self.FileName = ""
        self.FileDirectory = ""
        self.FilePath = ""
