import pyttsx3, threading, queue
class Mouth(object):
    """This class is used to convert text into speech through a configured audio device"""

    def __init__(self, luna):
        self.Queue = queue.Queue()
        self.IsMute = False
        self.SpeakThread = threading.Thread(target=self.mouthWorker, daemon=True)
        self.SpeakThread.start()
        self.Luna = luna

    def Speak(self, textToSpeak):
        self.Queue.put(textToSpeak)

    def Mute(self):
        self.Mute = True

    def UnMute(self):
        self.Mute = False

    def mouthWorker(self):
        while True:
            textToSpeak = self.Queue.get()
            engine = pyttsx3.init()
            engine.say(textToSpeak)
            engine.runAndWait();
            print('Said: ' + textToSpeak)
