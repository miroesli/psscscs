from numpy import array
from numpy.random import choice


class Agent:

    def __init__(self, nnet, training=False):
        self.nnet = nnet
        self.training = training
        self.records = []
        self.policies = []
        self.moves = []

    def make_move(self, state):
        X = array(state)
        values = self.nnet.pi(X)
        move = choice([0, 1, 2, 3], p=values)
        if self.training:
            # in reverse order
            # record the game state for traininig
            self.records.insert(0, X)
            # record the policy calculated by the network
            self.policies.insert(0, values)
            # record the move made
            self.moves.insert(0, move)
        return move

    def clear(self):
        self.records = []
        self.policies = []
