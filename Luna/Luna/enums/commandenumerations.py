from enum import IntEnum
class eCommandAction(IntEnum):
    """This describes what action to perform"""
    NONE = 0,
    OPEN = 1,
    CLOSE = 2,
    CREATE = 3,
    DELETE = 4,
    PLAY = 5,
    PAUSE = 6,
    SEARCH = 7,
    UNLOCK = 8,
    FOCUS = 9,
    MUTE = 10,
    UNMUTE = 11

class eCommandSearchType(IntEnum):
    """This is the type of search the command is to use"""
    NONE = 0,
    FILES = 1,
    DIRECTORIES = 2,
    ONLINE = 3,
    NETWORK = 4

class eCommandType(IntEnum):
    """This indicates what the command will be executing against"""
    LUNA = 0,
    APPLICATION = 1,
    MOBILE = 2,
    SERVICE = 3,
    WEB = 4,
    SEARCH = 5,
