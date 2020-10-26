class CommandAction(object):
    '''This is the main action object used when processing text into commands.  It holds on to important information such as the trigger text and the text that follows'''

    def __init__(self):
        self.TriggerText = ''
        self.TriggerTag = ''
        self.ProcedingText = ''
        self.Application = []
