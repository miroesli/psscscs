from numpy import array, argmax
from numpy.random import choice

EMPTY = 0.0
WALL = 1.0
# adders & mutipliers
# (value + value_a) * value_m
HUNGER_a = -101
HUNGER_m = 0.01
SNAKE_m = 0.01


class Agent:
    
    def __init__(self, nnet, snake_ids, training=False):
        self.nnet = nnet
        self.training = training
        self.records = {i:[] for i in snake_ids}
        self.policies = {i:[] for i in snake_ids}
        self.moves = {i:[] for i in snake_ids}
    
    def make_moves(self, states, snake_ids):
        X = array(states)
        Y = self.nnet.pi(X)
        if self.training:
            moves = [choice([0, 1, 2, 3], p=y) for y in Y]
            for i in range(len(states)):
                # record the game state for traininig
                self.records[snake_ids[i]].append(X[i])
                # record the policy calculated by the network
                self.policies[snake_ids[i]].append(Y[i])
                # record the move made
                self.moves[snake_ids[i]].append(moves[i])
        else:
            moves = [argmax(y) for y in Y]
        return moves
    
    def clear(self):
        for i in self.records:
            self.records[i] = []
            self.policies[i] = []
            self.moves[i] = []