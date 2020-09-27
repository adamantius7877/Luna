from vosk import Model, KaldiRecognizer, SetLogLevel
#from pocketsphinx import LiveSpeech
import os
import threading
import pyaudio

class Ears(object):
    """This class is used to listen t wo audio sources and interpet them into text"""

    def __init__(self, luna):
        self.IsListening = False
        self.Buffer = 8000
        self.Rate = 16000
        self.Channels = 1
        self.Model = Model("model_small")
        self.Rec = KaldiRecognizer(self.Model, self.Rate)
        self.Luna = luna
        self.Stream = []

    def callback(self, in_data, frame_count, time_info, status):
        if len(in_data) > 0 and self.Rec.AcceptWaveform(in_data):
            result = self.Rec.Result()
            self.Luna.Brain.InterpretCommand(result)
        return (in_data, pyaudio.paContinue)

    def __InnerListen(self):
        self.IsListening = True
        SetLogLevel(-1)
        p = pyaudio.PyAudio()
        self.Stream = p.open(format=pyaudio.paInt16, channels=self.Channels, rate=self.Rate, input=True, frames_per_buffer=self.Buffer, stream_callback=self.callback)
        self.Stream.start_stream()
        #for phrase in LiveSpeech(): print(phrase)

       #while self.IsListening:
       #    data = stream.read(self.Buffer)
       #    if len(data) == 0:
       #        break
       #    if self.Rec.AcceptWaveform(data):
       #        result = self.Rec.Result()
       #        self.Luna.Brain.InterpretCommand(result)

    def Listen(self):
       self.Thread = threading.Thread(target=self.__InnerListen, daemon=True) 
       self.Thread.start()

    def StopListening(self):
        self.IsListening = False
        self.Thread._stop()
