class Agent:

    def __init__(self, nnet, training = False):
        self.nnet = nnet
        self.training = training
        self.records = []
    
    def make_move(self, game, snake):
        if self.training:
            # record the game state for traininig
            self.records.append(grid.deepcopy())
        return nnet.eval(grid)
