import argparse

parser = argparse.ArgumentParser(prog='Luna', description='Luna, Lexical Universal Natural Assistant')

parser.add_argument('--install', help='Install and setup Luna and all requirements')
parser.add_argument('--config', action='store', dest='config', help='The path to the user\'s config file', default='luna-default.json')
parser.add_argument('--command', action='store', dest='runCommand', help='Run a single command')
parser.add_argument('--status', dest='status', help='Get the current status of Luna', default=False)

results = parser.parse_args()

print(results)

if len(results.runCommand) > 0:
    from src.brain.neurons.nerve import Nerve
    from src.brain.lobe import Lobe
    import src.common.constants as constants
    with Nerve(Lobe()) as nerve:
        nerve.Ending = constants.CNS_COMMAND_CHANNEL
        nerve.Stimulate(results.runCommand)
