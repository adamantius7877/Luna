from .nerve import Nerve
from ...common import constants

class MouthNerve(Nerve):
    '''This is the primary commmunication nerve for the mouth'''

    def __init__(self, lobe):
        super().__init__(lobe)
        self.Ending = constants.CNS_MOUTH_CHANNEL

    def __enter__(self):
        return super().__enter__(self)

    def __exit__(self,*_):
        pass
