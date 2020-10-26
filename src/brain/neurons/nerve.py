from .datapackage import DataPackage
import redis, threading, json

class Nerve(object):
    """This is a wrapper object for dealing with redis channels for the rest of the system"""

    def __init__(self, parentLobe):
        self.AcceptAll = False
        self.Whitelist = []
        self.Ending = ""
        self.Receptor = []
        self.IsActive = False
        self.Lobe = parentLobe
        self.Redis = redis.Redis(host=self.Lobe.RedisHost, port=self.Lobe.RedisPort, db=self.Lobe.RedisDB)
        self.RedisPubSub = self.Redis.pubsub()
        self.RedisThread = []

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.Shutdown()

    def Activate(self, receptor):
        print("Activated " + self.Ending)
        self.Receptor = receptor
        self.RedisPubSub.subscribe(**{self.Ending:self.Stimulated})
        self.RedisThread = self.RedisPubSub.run_in_thread(sleep_time=0.001)
        self.IsActive = True

    def Deactivate(self):
        if self.RedisPubSub:
            self.RedisPubSub.unsubscribe()
        if self.RedisThread:
            self.RedisThread._stop()
        self.IsActive = False

    def Stimulate(self, data):
        dataPackage = DataPackage(self.Lobe, data)
        encoder = json.JSONEncoder()
        dataPackageJson = encoder.encode([self.Lobe.IPV4Address,data])
        self.Redis.publish(self.Ending, dataPackageJson)
        print("Stimulated nerve ")# + self.Ending)

    def Stimulated(self, data):
        dataPackageJson = bytes.decode(data["data"], 'utf-8')
        if isinstance(dataPackageJson, str):
            decoder = json.JSONDecoder()
            dataPackage = decoder.decode(dataPackageJson)
            if self.AcceptAll or dataPackage[0] == self.Lobe.IPV4Address or self.InWhitelist(dataPackage[0]):
                #print(self.Ending + " has been stimulated with '" + dataPackage[1] + "'")
                self.Receptor(dataPackage[1])
            else:
                print("Attempted stimulation from " + dataPackage[0] + " with data " + dataPackage[1])

    def Shutdown(self):
        self.Deactivate()
        self.Redis.close()

    def InWhitelist(self, itemToCheck):
        for address in self.Whitelist:
            if address == itemToCheck:
                return True
        return False

