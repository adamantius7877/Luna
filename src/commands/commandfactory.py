from .command import Command
from ..common.application import Application
from .applicationcommand import ApplicationCommand
from .lunacommand import LunaCommand
from .commandidentifier import *
from ..common.processedsentence import ProcessedSentence
from ..common import constants
from ..brain.neurons import centralnerve
import nltk

class CommandFactory(object):
    '''This is the base factory used to process text, interpret the results, and create commands based off of it.'''

    def __init__(self, lobe):
        self.Lobe = lobe
        self.CentralNerve = centralnerve.CentralNerve(self.Lobe)
        self.CentralNerve.Activate(self.GetCentralNerveData)
        self.Identifiers = []
        self.PopulateIdentifiers()
        self.Applications = []

    def __enter__(self):
        return self

    def __exit__(self,*_):
        pass

    def GetPossibleCommands(self, textToProcess):
        possibleCommands = []
        processedSentence = self.GetProcessedSentence(textToProcess)

        identifierFound = False
        possibleIdentifiers = []

        innerText = ''

        # Go through all the text, in order, and match any keywords
        for tag in processedSentence.Tags:
            tagValue = tag[0]
            tagType = tag[1]
            if identifierFound:
                # We must check all identifiers for possible tags for their ending and add 
                # that as a possible command 
                identifiersToRemove = []
                for identifier in possibleIdentifiers:
                    if tagType in identifier.MajorTags or tagValue in identifier.Keywords:
                        identifier.SelectedTag = tagType
                        identifier.SelectedKeyword = tagValue
                        command = self.GetCommandFromIdentifier(identifier, innerText)
                        possibleCommands.append(command)
                        identifiersToRemove(identifier)

                # Remove any identifiers where we found it's next tag
                for identifier in identifiersToRemove:
                    possibleIdentifiers.remove(identifier)

                # Reassess if we are still looking into an identifier
                identifierFound = len(possibleIdentifiers) > 0
                if identifierFound:
                    innerText += ' ' + tagValue
            else:
                possibleIdentifiers = self.GetPossibleIdentifiers(tagValue, tagType)
                if len(possibleIdentifiers) > 0:
                    identifierFound = True
        if identifierFound:
            innerText = innerText.strip()
            for identifier in possibleIdentifiers:
                command = self.GetCommandFromIdentifier(identifier, innerText)
                possibleCommands.append(command)


        return possibleCommands

    def GetCommandFromIdentifier(self, identifier, innerText):
        if identifier.Type == constants.APPLICATION_COMMAND_TYPE:
            command = ApplicationCommand(identifier)
        elif identifier.Type == constants.LUNA_COMMAND_TYPE:
            command = LunaCommand(identifier)
        if command:
            command.ProccessInnerText(innerText)
            command.FinishProcessing()
            return command
        else:
            return None

    def GetProcessedSentence(self, textToProcess):
        processedSentence = ProcessedSentence() 
        if(len(textToProcess) == 0): 
            processedSentence.Errors.append("No sentence provided")
            return processedSentence
        processedSentence.Sentence = textToProcess
        processedSentence.Tokens = nltk.word_tokenize(textToProcess)
        processedSentence.Tags = nltk.pos_tag(processedSentence.Tokens)
        return processedSentence

    def GetPossibleIdentifiers(self, tagValue, tagType):
        possibleIdentifiers = []
        for identifier in self.Identifiers:
            if tagValue.lower() in identifier.Keywords:
                identifier.SelectedKeyword = tagValue
                identifier.SelectedTag = tagType
                possibleIdentifiers.append(identifier)
        return possibleIdentifiers

    def GetCentralNerveData(self, data):
        if data == constants.GET_ALL_APPLICATIONS_NERVE_MESSAGE:
            pass
        for identifier in self.Identifiers:
            if identifier.Type == constants.APPLICATION_COMMAND_TYPE:
                for application in data:
                    if application == constants.GET_ALL_APPLICATIONS_NERVE_MESSAGE:
                        continue
                    app = Application()
                    app.ID = application[1]
                    app.Path = application[2]
                    app.Name = application[0]
                    identifier.Applications.append(app)
                    if application[0] not in identifier.TargetKeywords:
                        identifier.TargetKeywords.append(application)

    def PopulateIdentifiers(self):
        self.Identifiers.append(LunaCommandIdentifier())
        applicationIdentifier = ApplicationCommandIdentifier()
        self.Identifiers.append(applicationIdentifier)
        self.CentralNerve.Stimulate([constants.GET_ALL_APPLICATIONS_NERVE_MESSAGE,])
