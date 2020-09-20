from mouth import Mouth
from eyes import Eyes
from ears import Ears
from brain import Brain

class Luna(object):
    """Lexical Univeral Natural Assistant, or Luna"""
    class __Luna(object):
        def __init__(self):
            self.val = None
            self.Ears = Ears()
            self.Mouth = Mouth()
            self.Brain = Brain()
            self.Eyes = Eyes()
            self.IsRunning = False
        
        def Start(self):
            if self.IsRunning:
                return
            self.IsRunning = True
            self.Mouth.Speak("Systems booting")
            self.Ears.Listen()
            self.Mouth.Speak("Good to be back, sir")

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
