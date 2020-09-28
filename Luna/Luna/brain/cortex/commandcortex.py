from common.command import Command
from brain.neurons.textprocessingneuron import TextProcessingNeuron
from enums.commandenumerations import eCommandType, eCommandAction, eCommandSearchType
import json, common, redis
from common import constants, config

class CommandCortex:
    """This is the cortex that controls processing and interpreting commands"""

    def __init__(self):
        self.AllCommands = []
        self.AvailableCommands = []
        self.AllApplicationCommands = []
        self.AvailableApplicationCommands = []
        self.DefaultCommands = []
        self.__RefreshCommandActions()
        self.TextProcessingNeuron = TextProcessingNeuron(self.CommandActions);
        self.__GetDefaultComands()
        self.Redis = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
        self.RedisPubSub = self.Redis.pubsub()
        self.RedisPubSub.subscribe(**{constants.REDIS_EAR_CHANNEL:self.InterpretCommand})
        self.RedisThread = self.RedisPubSub.run_in_thread(sleep_time=0.001)

    def InterpretCommand(self, textToInterpret):
        processedText = str(textToInterpret["data"]) #self.ProcessText(textToInterpret)
        if len(processedText) == 0:
            return None
        processedSentence = self.TextProcessingNeuron.ProcessSentence(processedText)
        if not processedSentence.IsLunaSubject: return None
        self.Redis.publish("mouth-channel", "Processed " + processedText)
        command = Command()
        for action in processedSentence.Actions:
            actionStart = action[0]
            actionText = action[1]
            command.CommandAction = action[2]
            if command.CommandAction == eCommandAction.SEARCH:
                if actionText.find("online") >= 0 or actionText.find("google") >= 0:
                    command = self.__GetCommand(config.DEFAULT_BROWSER_COMMAND_NAME)
                    command.Arguments = constants.GOOGLE_QUERY_BASE + actionText
                else:
                    command.CommandType = eCommandType.SEARCH
                    command.SearchText = actionText
                    command.Path = constants.HOME_DIRECTORY
                break
            elif command.CommandAction == eCommandAction.FOCUS or\
                 command.CommandAction == eCommandAction.PAUSE or\
                 command.CommandAction == eCommandAction.PLAY:
                command.CommandType = eCommandType.LUNA
                command.Name = actionText
                break
            else:
                command = self.__GetCommand(actionText)
                break
            break

        return command

    def ProcessText(self, textToProcess):
        print(str(textToProcess["data"]))
        if textToProcess.find('{') < 0:
            return textToProcess;
        textObject = json.loads(textToProcess)
        text = textObject["text"]
        if len(text) > 0:
            print(text)
        return text.lower()

    def __GetCommand(self, possibleName):
        command = self.__GetCommandFromList(possibleName, self.AvailableApplicationCommands)
        if command is None:
            command = self.__GetCommandFromList(possibleName, self.DefaultCommands)
        return command

    def __GetCommandFromList(self, possibleName, listOfPossibilities):
        for command in listOfPossibilities:
            if command.Name == possibleName:
                return self.GetCopy(command)
            else:
                for alias in command.Aliases:
                    if alias == possibleName:
                        return command
        return None


    def __RefreshCommandActions(self):
        self.CommandActions = [
        ["open",["launch","run"],eCommandAction.OPEN],
        ["add",[""],eCommandAction.ADD],
        ["create",[""],eCommandAction.CREATE],
        ["close",["exit"],eCommandAction.CLOSE],
        ["pause",[""],eCommandAction.PAUSE],
        ["play",["continue"],eCommandAction.PLAY],
        ["unlock",[""],eCommandAction.UNLOCK],
        ["search",["find", "look", "hunt"],eCommandAction.SEARCH],
        ["switch",[""],eCommandAction.FOCUS],
        ]

    def __GetDefaultComands(self):
        command = Command()
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

    def GetExecutableSearchCommandForPath(self, path, extension):
        command = Command()
        command.Path = path
        command.CommandType = eCommandType.SEARCH
        command.CommandAction = eCommandAction.SEARCH
        command.SearchType = eCommandSearchType.FILES
        command.SearchExtension = extension
        command.SearchText = "*"
        return command

    def GetExecutableSearchCommandsForPath(self, paths, extension):
        commands = []
        for path in paths:
            commands.append(self.GetExecutableSearchCommandForPath(path, extension))
        return commands

    def GetCommandsForApplicationPaths(self, applicationSearchResults):
        commands = []
        for applicationSearchResult in applicationSearchResults:
            commands.append(self.GetCommandForApplicationPath(applicationSearchResult))
        return commands

    def GetCommandForApplicationPath(self, applicationSearchResult):
        command = Command()
        command.Path = applicationSearchResult.FileDirectory
        command.Name = applicationSearchResult.FileName
        command.CommandType = eCommandType.APPLICATION
        command.CommandAction = eCommandAction.OPEN
        command.SearchType = eCommandSearchType.NONE
        command.SearchExtension = ""
        command.SearchText = ""
        return command

    def GetApplicationCommandFromJsonObject(self, jsonCommand):
        command = Command()
        command.Path = jsonCommand["Path"]
        command.Name = jsonCommand["Name"]
        command.CommandType = jsonCommand["CommandType"]
        command.CommandAction = jsonCommand["CommandAction"]
        command.SearchType = jsonCommand["SearchType"]
        command.SearchExtension = jsonCommand["SearchExtension"]
        command.SearchText = jsonCommand["SearchText"]
        return command

    def GetJsonObjectFromApplicationCommand(self, command):
        jsonObject = {
        "Path" : command.Path,
        "Name" : command.Name,
        "CommandType" : str(command.CommandType),
        "CommandAction" : str(command.CommandAction),
        "SearchType" : str(command.SearchType),
        "SearchExtension" : command.SearchExtension,
        "SearchText" : command.SearchText,
        }
        return jsonObject

    def FindApplicationCommandsByName(self, applicationName, allowMultiple):
        results = []
        for applicationCommand in self.AllApplicationCommands:
            if applicationCommand.Name.lower().find(applicationName.lower()) >= 0:
                results.append(applicationCommand)
                if not allowMultiple:
                    return results
        return results

    def FindApplicationCommandsByDirectory(self, directoryName, allowMultiple):
        results = []
        for applicationCommand in self.AllApplicationCommands:
            if applicationCommand.Path.lower().find(directoryName.lower()) >= 0:
                results.append(applicationCommand)
                if not allowMultiple:
                    return results
        return results

    def SetAvailableApplicationCommands(self, listOfApplications):
        for applicationName in listOfApplications:
            for applicationCommand in self.AllApplicationCommands:
                if applicationCommand.Name == applicationCommand:
                    self.AddAvailableCommand(applicationCommand)

    def AddAvailableCommand(self, command):
        for availableCommand in self.AvailableCommands:
            if availableCommand.Name == command.Name:
                return
        self.AvailableCommands.append(command)
