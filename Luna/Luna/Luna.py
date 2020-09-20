from brain import Brain
from ears import Ears
from mouth import Mouth
from eyes import Eyes

class Luna(object):
    """Lexical Univeral Natural Assistant, or Luna"""
    class __Luna(object):
        def __init__(self):
            self.val = None
            self.Brain = Brain(self)
            self.Ears = Ears(self)
            self.Mouth = Mouth(self)
            self.Eyes = Eyes(self)
            self.Mouth.Speak("All systems online.  It's good to be back.")
            self.IsRunning = False
            self.IsInitialized = True
        
        def Start(self):
            if self.IsRunning:
                return
            self.IsRunning = True
            self.Ears.Listen()

        def Stop(self):
            self.IsRunning = False
            self.Ears.StopListening()

        def Close(self):
            self.Stop()
            self.IsClosing = True

    instance = None
    def __init__(self):
        if not Luna.instance:
            Luna.instance = Luna.__Luna()

    def __getattr__(self, name):
        return getattr(self.instance,name)

while True:
    luna = Luna()
    luna.instance.Start()
    waitInput = input()
