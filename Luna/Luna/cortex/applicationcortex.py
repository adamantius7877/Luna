from command import Command
import os

class ApplicationCortex:
    """This cortex deals with running and managing applications"""
    
    def __init__(self):
        self.Processes = []
        self.DefaultCommands = []

    def RunCommand(self, command):
        path = command.fullPath()
        arguments = command.Arguments
        #command.AssociatedProcess.append(subprocess.run([path, arguments]))
        os.startfile(path)

    def StopCommand(self, command):
        return



