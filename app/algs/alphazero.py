from utils.agent import Agent
from utils.game import Game
from utils.AlphaNNet import AlphaNNet
import numpy as np

# https://web.stanford.edu/~surag/posts/alphazero.html


class AlphaZeroTrainer:
    def __init__(self, numIters=100000,
                 numEps=1000,
                 competeEps=100,
                 threshold=0.55,
                 height=11,
                 width=11,
                 player_cnt=8,
                 food_spawn_period=0,
                 **config):
        print(type(numIters))
        self.numIters = numIters
        self.numEps = numEps
        self.competeEps = competeEps
        self.threshold = threshold
        self.height = height
        self.width = width
        self.player_cnt = player_cnt
        self.food_spawn_period = food_spawn_period

    def train_alpha(self, nnet):
        # for training, all agents uses the same nnet
        # unless we want to use a evolution algorithm
        agents = [Agent(nnet, training=True) for _ in range(self.player_cnt)]
        for i in range(self.numIters):
            X = []
            Y = []
            # the loop below can use distributed computing
            for e in range(self.numEps):
                # collect examples from a new game
                g = Game(self.height, self.width, self.player_cnt,
                         self.player_cnt, self.food_spawn_period)
                winner_id = g.run(agents)
                for i in range(len(agents)):
                    agent = agents[i]
                    X += agent.records
                    if i == winner_id:
                        pass    # TODO
                    else:
                        pass    # TODO
                    agent.clear()
            new_nnet = nnet.copy()
            new_nnet.train(np.array(X), np.array(Y))
            # compare new net with previous net
            frac_win = compete(new_nnet, nnet)
            if frac_win > threshold:
                # replace with new net
                nnet = new_nnet
                print("Iteration", i, "beats the previouse version with a WR of",
                      frac_win, "\nIt is now the new champion!\n")
            else:
                print("Iteration", i, "failed to beat the previouse one.\n")
        return nnet

    def train(self):
        nnet = AlphaNNet(in_shape=(self.player_cnt, self.height, self.width))
        num = 0
        while 1:
            num += 1
            nnet = self.train_alpha(nnet)
            # need to store the nnet
            nnet.save("Network No." + str(num))

    def compete(self, nnet1, nnet2):
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
        return wins/self.competeEps
