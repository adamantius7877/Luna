from ..neurons.commandnerve import CommandNerve
from ..neurons.mouthnerve import MouthNerve
from ..neurons.nerve import Nerve
from ..lobe import Lobe
from ...commands.commandfactory import CommandFactory

import nltk

class CommandCortex(object):
    '''The cortex that handles processing commands received from the central nervous system'''

    def __init__(self, lobe):
        self.Lobe = lobe
        self.CommandNerve = CommandNerve(self.Lobe)
        self.CommandNerve.AcceptAll = True
        self.MouthNerve = MouthNerve(self.Lobe)
        self.CommandFactory = CommandFactory(self.Lobe)

    def __enter__(self):
        return self

    def __exit__(self,*_):
        pass

    def ProcessCommand(self, commandToProcess):
        print("Processing " + commandToProcess)
        commands = self.CommandFactory.GetPossibleCommands(commandToProcess)
        if commands:
            for command in commands:
                command.Print()
        else:
            print('No commands found')
        print("Finished processing " + commandToProcess)
            
        self.MouthNerve.Stimulate(commandToProcess)

    def Activate(self):
        self.CommandNerve.Activate(self.ProcessCommand)

    def Deactivate(self):
        self.CommandNerve.Deactivate()
