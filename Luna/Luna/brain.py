from command import Command

class Brain(object):
    """description of class"""
    def __init__(self, luna):
        self.Luna = luna

    def InterpretCommand(self, textToInterpret):
        command = Command()
        self.Luna.Mouth.Speak("I am interpreting the command")
        return command
