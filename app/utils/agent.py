from numpy import reshape, argmax
from numpy.random import choice


class Agent:
    
    def __init__(self, nnet, snake_ids, training=False):
        self.nnet = nnet
        self.training = training
        if training:
            self.records = {i:[] for i in snake_ids}
            self.policies = {i:[] for i in snake_ids}
            self.moves = {i:[] for i in snake_ids}
    
    def make_moves(self, states, snake_ids):
        X = reshape(states, (-1, len(states[0]), len(states[0][0]), 3))
        Y = self.nnet.pi(X)
        if self.training:
            moves = [choice([0, 1, 2, 3], p=y) for y in Y]
            for i in range(len(states)):
                # record the game state for traininig
                self.records[snake_ids[i]].insert(0, X[i])
                # record the policy calculated by the network
                self.policies[snake_ids[i]].insert(0, Y[i])
                # record the move made
                self.moves[snake_ids[i]].insert(0, moves[i])
        else:
            moves = [argmax(y) for y in Y]
        return moves
    
    def clear(self):
        for i in self.records:
            self.records[i] = []
            self.policies[i] = []
            self.moves[i] = []
