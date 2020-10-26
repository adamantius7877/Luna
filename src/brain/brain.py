from .lobe import Lobe
from .cortices import commandcortex
from .cortices import oscortex

class Brain(object):
    """The primary manager of Luna for the current device"""

    def __init__(self):
        self.Cortices = []
        self.Nerves = []
        self.Lobe = []
        self.__Initialize()
        self.IsAlive = True

    def __enter__(self):
        return self

    def __exit__(self,*_):
        pass

    def __Initialize(self):
        self.__GetLobe()
        self.__LoadConfiguration()
        self.__LoadCortices()

    def __GetLobe(self):
        self.Lobe = Lobe()

    def __LoadConfiguration(self):
        pass

    def __LoadCortices(self):
        osCortex = oscortex.OSCortex(self.Lobe)
        osCortex.Activate()
        commandCortex = commandcortex.CommandCortex(self.Lobe)
        commandCortex.Activate()
        self.Cortices.append(commandCortex)
        self.Cortices.append(osCortex)
