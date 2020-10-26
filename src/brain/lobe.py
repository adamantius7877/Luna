from ..config.config import Config
import socket, re, uuid

class Lobe(object):
    """Representation of a node on the current network"""

    def __init__(self):
        self.Configuration = Config()
        self.RedisDB = 0
        self.Name = socket.gethostname()
        self.IPV4Address = ''
        self.MacAddress = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
        self.RedisHost = self.Configuration.REDIS_SERVER #"87.87.10.228"
        self.RedisPort = self.Configuration.REDIS_PORT #6379
        self.GetIP4Address()

    def GetIP4Address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        self.IPV4Address = IP




