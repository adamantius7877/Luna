from .command import Command
from .commandquestion import CommandQuestion
from ..common import constants


class LunaCommand(Command):
    '''This is the command type specifically based to handle commands for Luna itself'''

    def __init__(self, commandIdentifier):
        super().__init__(commandIdentifier)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        pass

    def Execute(self):
        if self.Action in constants.INSTALL_ACTION_NAMES:
            ExecuteInstall()
        elif self.Action in constants.SETUP_ACTION_NAMES:
            ExecuteSetup()
        elif self.Action in constants.CONFIG_ACTION_NAMES:
            ExecuteConfig()
        elif self.Action in constants.UNINSTALL_ACTION_NAMES:
            ExecuteUninstall()

    def ExecuteInstall(self):
        pass

    def ExecuteSetup(self):
        pass

    def ExecuteConfig(self):
        pass

    def ExecuteUninstall(self):
        pass

    def ExecuteStatus(self):
        pass

