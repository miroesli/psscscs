from numpy import array, argmax

from utils.agent import Agent
from utils.game import Game
from utils.alphaNNet import AlphaNNet

# https://web.stanford.edu/~surag/posts/alphazero.html


class AlphaSnakeZeroTrainer:
    
    def __init__(self, numIters=1,
                 numEps=100,
                 competeEps=100,
                 threshold=0.55,
                 height=11,
                 width=11,
                 player_cnt=8,
                 model=None,
                 **config):

        self.numIters = numIters
        self.numEps = numEps
        self.competeEps = competeEps
        self.threshold = threshold
        self.height = height
        self.width = width
        self.player_cnt = player_cnt
        self.model = model

    def train_alpha(self, nnet):
        # for training, all agents uses the same nnet
        # unless we want to use a evolution algorithm
        agents = [Agent(nnet, training=True) for _ in range(self.player_cnt)]
        for iter in range(self.numIters):
            X = []
            Y = []
            # the loop below can use distributed computing
            for ep in range(self.numEps):
                # collect examples from a new game
                g = Game(self.height, self.width, self.player_cnt)
                winner_id = g.run(agents)
                for i in range(len(agents)):
                    agent = agents[i]
                    X += agent.records
                    # assign estimated policies
                    # this substitutes the MCTS
                    step = len(agent.policies)
                    if i == winner_id:
                        for j in range(step):
                            index = agent.moves[j]
                            decay = [0] * 4
                            boost = 0
                            for k in range(4):
                                if k != index:
                                    decay[k] = agent.policies[j][k]*(j + 1)/step
                                    boost += decay[k]
                            for k in range(4):
                                if k == index:
                                    agent.policies[j][k] += boost
                                else:
                                    agent.policies[j][k] -= decay[k]
                    else:
                        for j in range(step):
                            index = agent.moves[j]
                            decay = agent.policies[j][index]*(j + 1)/step
                            boost = decay/3
                            for k in range(4):
                                if k == index:
                                    agent.policies[j][k] -= decay
                                else:
                                    agent.policies[j][k] += boost
                    Y += agent.policies
                    agent.clear()
            new_nnet = nnet.copy()
            new_nnet.train(array(X), array(Y))
            # compare new net with previous net
            frac_win = self.compete(new_nnet, nnet)
            if frac_win > self.threshold:
                # replace with new net
                nnet = new_nnet
                print("Iteration", iter, "beats the previouse version with a WR of", frac_win, "\nIt is now the new champion!\n")
            else:
                print("Iteration", iter, "failed to beat the previouse one. WR =", frac_win, "\n")
        return nnet

    def train(self):
        if self.model:
            nnet = AlphaNNet(model=self.model)
        else:
            nnet = AlphaNNet(in_shape=(self.player_cnt, self.height, self.width))
        model_num = 0
        while 1:
            model_num += 1
            nnet = self.train_alpha(nnet)
            # need to store the nnet
            nnet.save("Network_No." + str(model_num))
            print("Network saved.")

    def compete(self, nnet1, nnet2):
        agents = [None] * self.player_cnt
        sep = self.player_cnt//2
        for i in range(sep):
            agents[i] = Agent(nnet1)
        for i in range(sep, self.player_cnt):
            agents[i] = Agent(nnet2)
        win = 0
        loss = 0
        for _ in range(self.competeEps):
            g = Game(self.height, self.width, self.player_cnt)
            winner = g.run(agents)
            if winner is None:
                win += 1
                loss += 1
            elif winner < sep:
                win += 1
            else:
                loss += 1
        return win/(win + loss)
