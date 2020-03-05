from utils.agent import Agent
from utils.game import Game

# https://web.stanford.edu/~surag/posts/alphazero.html


class neuralnet:
    def __init__(self, numIters=100000,
                 numEps=1000,
                 competeEps=100,
                 threshold=0.55,
                 height=11,
                 width=11,
                 player_cnt=8, **config):

        self.numIters = numIters
        self.numEps = numEps
        self.competeEps = competeEps
        self.threshold = threshold
        self.height = height
        self.width = width
        self.player_cnt = player_cnt

    def train(self):
        # initialise neural network
        nnet = NNet()
        # TODO: Change this to iterations?
        while 1:
            # for training, all agents uses the same nnet
            # unless we want to use a evolution algorithm
            agents = [Agent(nnet, training=True)
                      for _ in range(self.player_cnt)]
            for _ in range(self.numIters):
                for _ in range(self.numEps):
                    # collect examples from a new game
                    g = Game(self.height, self.width, self.player_cnt)
                    winner_id = g.run(agents)
                    for agent in agents:
                        # return a new trained nnet
                        X = agent.records
                        # need to get a good loss function
                        Y = 0
                        new_nnet = nnet.copy()
                        new_nnet.trainNNet(X, Y)
                # compare new net with previous net
                frac_win = compete(new_nnet, nnet)
                if frac_win > self.threshold:
                    # replace with new net
                    nnet = new_nnet
        return nnet

    def compete(nnet1, nnet2):
        agents = [None] * self.player_cnt
        sep = self.player_cnt//2
        for i in range(sep):
            agents[i] = Agent(nnet1)
        for i in range(sep, player_cnt):
            agents[i] = Agent(nnet2)
        wins = 0
        for _ in range(self.competeEps):
            g = Game(self.height, self.width, self.player_cnt)
            if g.run(agents) < sep:
                wins += 1
        return win/self.competeEps
