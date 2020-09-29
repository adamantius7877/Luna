from common.command import Command
from common import config, constants
import pyttsx3, threading, queue, redis
class Mouth(object):
    """This class is used to convert text into speech through a configured audio device"""

    def __init__(self, luna):
        self.Queue = queue.Queue()
        self.IsMute = False
        self.SpeakThread = threading.Thread(target=self.mouthWorker, daemon=True)
        self.SpeakThread.start()
        self.Luna = luna
        self.Redis = redis.Redis(host=config.REDIS_HOST, port=config.REDIS_PORT, db=0)
        self.RedisPubSub = self.Redis.pubsub()
        self.RedisPubSub.subscribe(**{constants.REDIS_MOUTH_CHANNEL:self.ServiceMessage})
        self.RedisThread = self.RedisPubSub.run_in_thread(sleep_time=0.001)

    def ServiceMessage(self, data):
        message = str(data["data"])
        if len(message) > 0:
            self.Speak(message)

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

    def SpeakCommand(self, command):
        textToSpeak = ""
        if command.CommandAction == eCommandAction.OPEN:
            textToSpeak += "opening"

