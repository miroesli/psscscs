class Template:
    def __init__(self, iterations=100, **config):
        # default iterations are 100, but if specified in config, it is
        # overwritten.
        self.iterations = iterations
        print("Initialized configuration...")

    def train(self):
        print("Training...")
