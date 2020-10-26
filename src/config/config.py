import json

DEFAULT_CONFIG_LOCATION = 'src/config/default.json'

class Config(object):
    '''This is the primary global configuration file for the lobe'''


    def __init__(self):
        self.SPOKEN_NAME = ''
        self.REDIS_SERVER = ''
        self.REDIS_PORT = 0
        self.GetConfig()

    def GetConfig(self):
        with open(DEFAULT_CONFIG_LOCATION) as infile:
            data = json.load(infile)
        self.SPOKEN_NAME = data['name']
        self.REDIS_SERVER = data['redis_host']
        self.REDIS_PORT = data['redis_port']
