from brain.brain import Brain
from senses.ears import Ears
from senses.mouth import Mouth
from senses.eyes import Eyes
from common import config, constants
import redis

class Luna(object):
    """Lexical Univeral Natural Assistant, or Luna"""
    class __Luna(object):
        def __init__(self):
            self.val = None
            self.Brain = []
            self.Ears = []
            self.Mouth = []
            self.Eyes = []
            self.Redis = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
            self.IsRunning = False
            self.IsInitialized = True
        
        def StartPrimary(self):
            if self.IsRunning:
                return
            self.Brain = Brain(self)
            self.Ears = []
            self.Mouth = Mouth(self)
            self.Eyes = Eyes(self)
            self.Speak("Online.")
            self.IsRunning = False
            self.IsRunning = True

        def Stop(self):
            self.IsRunning = False
            self.Ears.StopListening()

        def Close(self):
            self.Stop()
            self.IsClosing = True

        def ListeningMode(self):
            self.Ears = Ears()
            self.Ears.Listen()

        def Speak(self, textToSpeak):
            self.Redis.publish("mouth-channel", textToSpeak)

        def InterpretCommand(self, commandText):
            self.Brain.InterpretCommand(commandText)

    instance = None
    def __init__(self):
        if not Luna.instance:
            Luna.instance = Luna.__Luna()

    def __getattr__(self, name):
        return getattr(self.instance,name)
