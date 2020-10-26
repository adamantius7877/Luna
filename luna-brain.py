from src.brain.brain import Brain
if __name__ == '__main__':
    with Brain() as brain:
        while brain.IsAlive:
            pass
