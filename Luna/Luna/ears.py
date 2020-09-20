from vosk import Model, KaldiRecognizer
import os
import threading
import pyaudio

class Ears(object):
    """This class is used to listen to audio sources and interpet them into text"""

    def __init__(self, luna):
        self.IsListening = False
        self.Buffer = 8000;
        self.Rate = 16000;
        self.Model = Model("model")
        self.Rec = KaldiRecognizer(self.Model, self.Rate)
        self.Luna = luna

    def __InnerListen(self):
        self.IsListening = True
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=self.Rate, input=True, frames_per_buffer=self.Buffer)
        stream.start_stream()

        while self.IsListening:
            data = stream.read(self.Buffer)
            if len(data) == 0:
                break
            if self.Rec.AcceptWaveform(data):
                result = self.Rec.Result()
                print(result)
                self.Luna.Brain.InterpretCommand(result)

    def Listen(self):
       self.Thread = threading.Thread(target=self.__InnerListen) 
       self.Thread.start()

    def StopListening(self):
        self.IsListening = False
        self.Thread._stop()
