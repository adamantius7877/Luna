class OSCortex(object):
    """This cortex handles dealing with Auto Hot Key"""

    def Mute(self):
        pass

    def Unmute(self):
        self.Mute()

    def SwitchActiveWindow(self, command):
        pass

    def TogglePlayPause(self):
        pass

    def GetExecutableExtension(self):
        return "sh"

    def GetDrives(self):
        allDrives = ['/']
        return allDrives
