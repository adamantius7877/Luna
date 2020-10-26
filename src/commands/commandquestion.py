class CommandQuestion(object):
    '''This is the representation of a question a command needs to have answered to get more information to execute'''

    def __init__(self):
        self.IsAnswered = False
        self.QuestionText = ''
        self.Question = []
        self.Answer = []

    def __enter__(self):
        return self

    def __exit__(self,*_):
        pass
