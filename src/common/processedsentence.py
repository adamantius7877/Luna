class ProcessedSentence(object):
    '''The return object for processing sentences in the text processing neuron'''

    def __init__(self):
        self.Errors = []
        self.Warnings = []
        self.Actions = []
        self.Tokens = []
        self.Tags = []
        self.Sentence = ""
        self.IsLunaSubject = False

