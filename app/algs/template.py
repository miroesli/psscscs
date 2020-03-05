class template:
    def __init__(self, **config):
        self.iterations = config['iterations']
        print("Initialized configuration...")

    def train(self):
        print("Training...")
