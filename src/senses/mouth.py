from ..brain.neurons.mouthnerve import MouthNerve

import queue, pyttsx3, threading

class Mouth(object):
    '''This is the 'voice' of the system and is where audio output is handled'''

    def __init__(self, lobe):
        self.IsAlive = True
        self.Lobe = lobe
        self.IsMute = False
        self.MouthNerve = MouthNerve(lobe)
        self.MouthNerve.Activate(self.Speak)
        self.Queue = queue.Queue()
        self.SpeakThread = threading.Thread(target=self.__speak__, daemon=True)
        self.SpeakThread.start()

    def __enter__(self):
        return self

    def __exit__(self,*_):
        pass

    def __speak__(self):
        while True:
            if not self.IsMute:
                textToSpeak = self.Queue.get()
                engine = pyttsx3.init()
                engine.say(textToSpeak)
                engine.runAndWait()
                print('Said: ' + textToSpeak)

    def Speak(self, textToSpeak):
        self.Queue.put(textToSpeak)
