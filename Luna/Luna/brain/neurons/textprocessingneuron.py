from common import constants
from enums.commandenumerations import eCommandType, eCommandAction, eCommandSearchType
import nltk

class TextProcessingNeuron(object):
    """This is the neuron that handles processing sentences into interpretable input"""

    def __init__(self, commandActions):
        self.CommandActions = commandActions

    def ProcessSentence(self, sentence):
        print("Processing " + sentence)
        processedSentence = ProcessedSentence() 
        if(len(sentence) == 0): 
            processedSentence.Errors.append("No sentence provided")
            return processedSentence
        processedSentence.Sentence = sentence
        processedSentence.Tokens = nltk.word_tokenize(sentence)
        processedSentence.Tags = nltk.pos_tag(processedSentence.Tokens)
        processedSentence.IsLunaSubject = self.ProcessTags(processedSentence)
        if processedSentence.IsLunaSubject:
            self.PrintTags(processedSentence)
            print(processedSentence.Actions)
        print("Finished processing " + sentence)
        return processedSentence

    def PrintTags(self, processedSentence):
        for tag in processedSentence.Tags:
            tagValue = tag[0]
            tagType = tag[1]
            print(tagValue + ":" + tagType)


    def ProcessTags(self, processedSentence):
        isValid = False
        inAction = False
        action = ["","",eCommandAction.NONE]
        for tag in processedSentence.Tags:
            tagValue = tag[0]
            tagType = tag[1]
            if(inAction):
                if tagType == "CC" or tagType == ".":
                    action[1] = action[1].strip()
                    processedSentence.Actions.append(action)
                    action = ["",""] 
                    inAction = False
                else:
                    action[1] += " " + tagValue
            elif tagValue.lower() == constants.LUNA_NAME.lower() and tagType == "NNP":
                isValid = True
            elif tagType == "VBP" or tagType == "VB" or tagType == "JJ": 
                commandActionSet = self.IsCommandAction(tagValue)
                if commandActionSet[0]:
                    action[0] = commandActionSet[1]
                    action[2] = commandActionSet[2]
                    inAction = True

        if inAction:
            action[1] = action[1].strip()
            processedSentence.Actions.append(action)
            
        return isValid

    def IsCommandAction(self, tagValue):
        for commandAction in self.CommandActions:
            commandActionValue = commandAction[0][0]
            commandActionSubvalueList = commandAction[0][1]
            commandActionEnum = commandAction[0][2]
            if tagValue == commandActionValue:
                return [True, commandActionValue, commandActionEnum]
            else:
                for commandSubAction in commandActionSubvalueList:
                    if tagValue == commandSubAction:
                        return [True, commandSubAction, commandActionEnum]
        return [False, "", ""]

class ProcessedSentence(object):
    """The return object for processing sentences in the text processing neuron"""

    def __init__(self):
        self.Errors = []
        self.Warnings = []
        self.Actions = []
        self.Tokens = []
        self.Tags = []
        self.Sentence = ""
        self.IsLunaSubject = False
