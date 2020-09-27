from ahk import AHK

from win32api import GetLogicalDriveStrings
from win32file import GetDriveType

import win32con


class OSCortex(object):
    """This cortex handles dealing with Auto Hot Key"""

    def __init__(self):
        self.AHK = AHK()

    def Mute(self):
        self.AHK.key_press(constants.MUTE_KEY)

    def Unmute(self):
        self.Mute()

    def SwitchActiveWindow(self, command):
        for window in self.AHK.windows():
            if window.title.lower().find(command.Name.encode('utf-8')) >= 0 or \
               window.text.lower().find(command.Name.encode('utf-8')) >= 0 or \
               window.class_name.lower().find(command.Name.encode('utf-8')) >= 0:
                window.activate()
                break

    def TogglePlayPause(self):
        self.AHK.show_tooltip("Luna: Pausing/Playing", second=2, x=10, y=10)
        for window in self.AHK.windows():
            if window.title.lower().find(b'youtube music') >= 0:
                activeWindow = self.AHK.active_window
                window.activate()
                self.AHK.key_press(constants.SPACE_KEY)
                activeWindow.activate()
                break;

    def GetExecutableExtension(self):
        return "exe"

    def GetDrives(self):
        allDrives = []
        drive_filters_examples = [
            (None, "All"),
            ((win32con.DRIVE_REMOVABLE,), "Removable"),
            ((win32con.DRIVE_FIXED, win32con.DRIVE_CDROM), "Fixed and CDROM"),
        ]
        for (drive_types_tuple, display_text) in drive_filters_examples:
            drives = self.__get_drives_list(drive_types=drive_types_tuple)
            for drive in drives:
                allDrives.append("{0:s}\\".format(drive))
        return allDrives

    def __get_drives_list(self, drive_types=(win32con.DRIVE_REMOVABLE,)):
        drives_str = GetLogicalDriveStrings()
        drives = [item for item in drives_str.split("\x00") if item]
        return [item[:2] for item in drives if drive_types is None or GetDriveType(item) in drive_types]