from numpy import array


class Agent:

    def __init__(self, nnet, training = False):
        self.nnet = nnet
        self.training = training
        self.records = []
        self.policies = []

    def make_move(self, state):
        X = array(state)
        values = self.nnet.pi(X)
        move = values.argmax()
        if self.training:
            # record the game state for traininig
            self.records.append(X)
            # record the policy calculated by the network
            self.policies.append(values)
        return move

    def clear(self):
        self.records = []
        self.policies = []
