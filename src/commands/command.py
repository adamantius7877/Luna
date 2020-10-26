from .commandaction import CommandAction
from ..common.application import Application
import nltk

class Command(object):
    '''This is the base object that all commands inherit off of in the system.  Think of it as the interface for the command system in Luna'''

    def __init__(self, commandIdentifier):
        self.Metadata = commandIdentifier
        self.Keywords = commandIdentifier.Keywords 
        self.SubKeywords = commandIdentifier.SubKeywords 
        self.TargetKeywords = commandIdentifier.TargetKeywords 
        self.Questions = []
        self.CommandRating = 0
        self.SubActions = []
        self.Action = commandIdentifier.SelectedKeyword
        self.Target = ''
        self.TargetType = commandIdentifier.Type
        self.Placement = 'default'
        self.Path = ''

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

    def Execute(self):
        pass

    def FinishProcessing(self):
        for subAction in self.SubActions:
            if len(self.Target) == 0 and subAction.TriggerTag == 'DT':
                self.Target = subAction.ProcedingText
            if len(self.Placement) == 0 and subAction.TriggerTag == 'IN':
                self.Placement = subAction.ProcedingText


    def ProccessInnerText(self, innerText):
        print('processing standard command inner text')
        self.Action = self.Metadata.SelectedKeyword
        self.TargetKeywords = self.Metadata.TargetKeywords
        print(self.TargetKeywords)
        print(innerText)
        tokenizedText = nltk.word_tokenize(innerText)
        taggedText = nltk.pos_tag(tokenizedText)
        markedTagTypes = ['DT','IN']
        inSubAction = False
        subAction = CommandAction()
        self.SubActions = []

        # Go through the tags and find the start of the sub command
        for tag in taggedText:
            tagValue = tag[0].strip()
            tagType = tag[1]

            justAdded = False
            # Go through all target keywords and check this value
            for targetKeyword in self.TargetKeywords:
                # The target was found indicating this is a sub action
                if tagValue == targetKeyword[0] and not justAdded:
                    inSubAction = True
                    subAction = CommandAction()
                    subAction.TriggerText = tagValue
                    subAction.TriggerTag = targetKeyword
                    self.SubActions.append(subAction)
                    self.Target = tagValue
                    justAdded = True
                    continue

            # Go through all marked tag types and check this tag
            for markedTagType in markedTagTypes:
                # The tag type was found indicating this is a sub action
                if tagType == markedTagType and not justAdded:
                    inSubAction = True
                    subAction = CommandAction()
                    subAction.TriggerText = tagValue
                    subAction.TriggerTag = tagType
                    self.SubActions.append(subAction)
                    justAdded = True
                    continue

            # Go through all key subwords and check this value
            for subKeyword in self.SubKeywords:
                # The value was found indicating this is a sub action
                if tagValue == subKeyword and not justAdded:
                    inSubAction = True
                    subAction = CommandAction()
                    subAction.TriggerText = tagValue
                    subAction.TriggerTag = tagType
                    self.SubActions.append(subAction)
                    justAdded = True
                    continue

            if inSubAction and not justAdded:
                subAction.ProcedingText += " " + tagValue


    def UpdateRating(self):
        answered = 0
        total = len(self.Questions)
        for question in self.Questions:
            if question.IsAnswered:
                answered+=1

        self.CommandRating = (answered / total) * 100

    def Print(self):
        print('Command Print')
        print('Action: ' + self.Action)
        print('Target: ' + self.Target)
        print('Target Type: ' + self.TargetType)
        print('Path: ' + self.Path)
        print('Placement: ' + self.Placement)
        print('End Command')
