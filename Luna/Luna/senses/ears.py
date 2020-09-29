from vosk import Model, KaldiRecognizer, SetLogLevel
from common import config, constants
#from pocketsphinx import LiveSpeech
import os, threading, pyaudio, redis, json, wave

class Ears(object):
    """This class is used to listen to audio sources and interpet them into text"""

    def __init__(self):
        self.IsListening = False
        self.Format = pyaudio.paInt16
        self.Buffer = 22050
        self.Rate = 44100
        self.Channels = 1
        self.Lock = threading.Lock()
        SetLogLevel(-1)
        self.Model = Model("model_small")
        self.Rec = KaldiRecognizer(self.Model, self.Rate)
        self.Stream = []
        self.Redis = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
        self.RedisPubSub = self.Redis.pubsub()
        self.RedisPubSub.subscribe(**{constants.REDIS_EAR_SERVICE_CHANNEL:self.ServiceMessage})
        self.RedisThread = self.RedisPubSub.run_in_thread(sleep_time=0.001)
        self.AlreadyRegistered = False
        self.InChildMode = False
        self.IsChildProcessing = False
        self.ChildFrameCount = 0

    def SetChildMode(self, setChildMode):
        self.InChildMode = setChildMode

    def ServiceMessage(self, data):
        message = int(data["data"])
        if message == 0:
            self.StopListening()
        elif message == 1:
            self.Listen()

    def ChildMessage(self, data):
        message = data["data"]
        with self.Lock:
            self.IsChildProcessing = True
        threading.Thread(target=self.ProcessAudio, args=(message, self.ChildFrameCount, self.ChildRecordingFile), daemon=True).start()

    def ChildRegister(self, data):
        if self.AlreadyRegistered: pass
        message = int(data["data"])
        self.ChildRecordingFile = wave.open("testchild.wav", "w")
        self.ChildRecordingFile.setsampwidth(2)
        self.ChildRecordingFile.setnchannels(self.Channels)
        self.ChildRecordingFile.setframerate(message)
        self.ChildFrameCount = message / 2
        self.AlreadyRegistered = True


    def callback(self, in_data, frame_count, time_info, status):
        if self.InChildMode:
            self.Redis.publish(constants.REDIS_EAR_CHILD_SERVICE_CHANNEL, (in_data))
        threading.Thread(target=self.ProcessAudio, args=(in_data,frame_count,self.RecordingFile), daemon=True).start()
        return (in_data, pyaudio.paContinue)

    def ProcessAudio(self, in_data, frame_count, recordingFile):
        with self.Lock:
            if frame_count > 0 and len(in_data) > 0:
                recordingFile.writeframes(in_data)
            if len(in_data) > 0 and self.Rec.AcceptWaveform(in_data):
                result = self.Rec.Result()
                sentence = self.ProcessText(result)
                if len(sentence) > 0:
                    self.Redis.publish("ear-channel", sentence)

    def __InnerListen(self):
        self.IsListening = True
        p = pyaudio.PyAudio()
        devindex = 0
        for i in range(p.get_device_count()):
            if p.get_device_info_by_index(i).get('name') == 'sysdefault':
                devindex = i
                break
        self.Rate = int(p.get_device_info_by_index(devindex).get('defaultSampleRate')) #44100
        self.Buffer = int(self.Rate / 2)
        print("Format: " + str(self.Format))
        print("Rate: " +  str(self.Rate))
        print("Buffer: " +  str(self.Buffer))
        print("Channels: " +  str(self.Channels))
        self.Stream = p.open(format=self.Format, channels=self.Channels, rate=self.Rate, input=True, frames_per_buffer=self.Buffer, stream_callback=self.callback)
        self.RecordingFile = wave.open("test.wav", "w")
        self.RecordingFile.setsampwidth(2)
        self.RecordingFile.setnchannels(self.Channels)
        self.RecordingFile.setframerate(self.Rate)
        if self.InChildMode:
            self.Redis.publish(constants.REDIS_EAR_CHILD_REGISTRATION_CHANNEL, (self.Rate))
        else:
            self.RedisPubSub.subscribe(**{constants.REDIS_EAR_CHILD_SERVICE_CHANNEL:self.ChildMessage})
            self.RedisPubSub.subscribe(**{constants.REDIS_EAR_CHILD_REGISTRATION_CHANNEL:self.ChildRegister})

        self.Stream.start_stream()
        print ("Listening")

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
