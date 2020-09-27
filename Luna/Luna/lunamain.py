from luna import Luna
import redis

lunaInstance = Luna()
lunaInstance.instance.StartPrimary()
waitInput = input()
