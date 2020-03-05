from numpy import array

class Agent:

    def __init__(self, nnet, training = False):
        self.nnet = nnet
        self.training = training
        self.records = []
        self.movess = []
    
    def make_move(self, state):
        X = array(state)
        values = self.nnet.eval(X)
        move = values.argmax()
        if self.training:
            # record the game state for traininig
            self.records.append(X)
            # record the move made by the agent
            self.moves.append(move)
        return move
    
    def clear(self):
        self.records = []
        self.moves = []
