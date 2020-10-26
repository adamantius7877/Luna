from src.senses.mouth import Mouth
from src.brain.lobe import Lobe
if __name__ == '__main__':
    with Mouth(Lobe()) as mouth:
        while mouth.IsAlive:
            pass
