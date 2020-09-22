from ahk import AHK
import constants

class AHKCortex(object):
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
