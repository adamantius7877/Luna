class DataPackage(object):
    '''This object holds all required information to be sent along the central nervous system'''

    def __init__(self, lobe, data):
        self.Lobe = lobe
        self.Data = data

    def __enter__(self):
        return self

    def __exit__(self,*_):
        pass
