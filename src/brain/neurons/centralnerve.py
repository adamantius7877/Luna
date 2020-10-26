from .nerve import Nerve
from ...common import constants

class CentralNerve(Nerve):
    '''This is the primary communication nerve for the central nervous system'''

    def __init__(self, lobe):
        super().__init__(lobe)
        self.Ending = constants.CNS_CENTRAL_CHANNEL
        

    def __enter__(self):
        return super().__enter__()

    def __exit__(self,*_):
        return super().__exit__(*_)
