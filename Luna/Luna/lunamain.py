from luna import Luna
import redis

lunaInstance = Luna()
lunaInstance.instance.StartPrimary()
lunaInstance.instance.ListeningMode()
waitInput = input()
