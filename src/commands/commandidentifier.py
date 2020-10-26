from ..common import constants 

class CommandIdentifier(object):
    '''This object represents the metadata for commands.  It is used in both breaking down text and populating the base information when creating commands.'''

    def __init__(self):
        self.SelectedKeyword = ''
        self.SelectedTag = ''
        self.SelectedSubKeyword = ''
        self.SelectedMinorTag = ''
        self.SelectedTargetKeyword = ''
        self.Keywords = []
        self.SubKeywords = []
        self.TargetKeywords = []
        self.MajorTags = ['CC','.']
        self.MinorTags = []
        self.Type = '' 

class ApplicationCommandIdentifier(CommandIdentifier):
    '''This object represents the metadata for the application command type'''

    def __init__(self):
        super().__init__()
        self.Keywords = ['open','launch','execute','run']
        self.SubKeywords = ['on','the']
        self.Type = constants.APPLICATION_COMMAND_TYPE
        self.Applications = []

class LunaCommandIdentifier(CommandIdentifier):
    '''This object represents the metadata for the luna command type'''

    def __init__(self):
        super().__init__()
        self.SubKeywords = ['on','the']
        self.TargetKeywords = ['brain','mouth','nerve','ears','service']
        self.Type = constants.LUNA_COMMAND_TYPE
        for keyword in constants.INSTALL_ACTION_NAMES:
            self.Keywords.append(keyword)
        for keyword in constants.SETUP_ACTION_NAMES:
            self.Keywords.append(keyword)
        for keyword in constants.CONFIG_ACTION_NAMES:
            self.Keywords.append(keyword)
        for keyword in constants.UNINSTALL_ACTION_NAMES:
            self.Keywords.append(keyword)
        for keyword in constants.STATUS_ACTION_NAMES:
            self.Keywords.append(keyword)
