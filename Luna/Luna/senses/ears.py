from vosk import Model, KaldiRecognizer, SetLogLevel
from common import config, constants
#from pocketsphinx import LiveSpeech
import os, threading, pyaudio, redis, json

class Ears(object):
    """This class is used to listen two audio sources and interpet them into text"""

    def __init__(self):
        self.IsListening = False
        self.Format = pyaudio.paInt16
        self.Buffer = 4096
        self.Rate = 44100
        self.Channels = 1
        SetLogLevel(-1)
        self.Model = Model("model_small")
        self.Rec = KaldiRecognizer(self.Model, self.Rate)
        self.Stream = []
        self.Redis = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
        self.RedisPubSub = self.Redis.pubsub()
        self.RedisPubSub.subscribe(**{constants.REDIS_EAR_SERVICE_CHANNEL:self.ServiceMessage})
        self.RedisThread = self.RedisPubSub.run_in_thread(sleep_time=0.001)

    def ServiceMessage(self, message):
        if message == 0:
            self.StopListening()
        elif message == 1:
            self.Listen()

    def callback(self, in_data, frame_count, time_info, status):
        if len(in_data) > 0 and self.Rec.AcceptWaveform(in_data):
            result = self.Rec.Result()
            sentence = self.ProcessText(result)
            if len(sentence) > 0:
                self.Redis.publish("ear-channel", sentence)
        return (in_data, pyaudio.paContinue)

    def __InnerListen(self):
        self.IsListening = True
        p = pyaudio.PyAudio()
        self.Stream = p.open(format=self.Format, channels=self.Channels, rate=self.Rate, input=True, frames_per_buffer=self.Buffer, stream_callback=self.callback)
        self.Stream.start_stream()

    def Listen(self):
       self.Thread = threading.Thread(target=self.__InnerListen, daemon=True) 
       self.Thread.start()

    def StopListening(self):
        self.IsListening = False
        self.Thread._stop()

    def ProcessText(self, textToProcess):
        if textToProcess.find('{') < 0:
            return textToProcess;
        textObject = json.loads(textToProcess)
        text = textObject["text"]
        if len(text) > 0:
            print(text)
        return text.lower()
