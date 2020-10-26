from .command import Command
from .commandaction import CommandAction

from .commandidentifier import ApplicationCommandIdentifier

import os, subprocess, nltk

class ApplicationCommand(Command):
    '''This is the base implementation for the command that will be responsible for handling execution of applications'''

    def __init__(self, commandIdentifier):
        super().__init__(commandIdentifier)
        commandIdentifier = ApplicationCommandIdentifier()
        self.Keywords = ['open','launch','execute','run']
        self.SubKeywords = ['on','the']
        self.Arguments = ''
        self.AssociatedProcess = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

    def Execute(self):
        #if len(self.Arguments) > 0:
        self.AssociatedProcess.append(subprocess.run([self.Path + self.Target, self.Arguments]))
        #else:
            #os.startfile(self.Path)
        #os.execv(self.Path + self.Action, [self.Action])

    def ProccessInnerText(self, innerText):
        super().ProccessInnerText(innerText)
        if len(self.Target) > 0:
            for application in self.Metadata.Applications:
                if application.Name == self.Target:
                    self.Path = application.Path
                    self.ApplicationID = application.ID
