from numpy import array, argmax
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
        if self.training:
            move = choice([0, 1, 2, 3], p=values)
            # in reverse order
            # record the game state for traininig
            self.records.append(X)
            # record the policy calculated by the network
            self.policies.append(values)
            # record the move made
            self.moves.append(move)
        else:
            move = argmax(values)
        return move

    def clear(self):
        self.records = []
        self.policies = []
