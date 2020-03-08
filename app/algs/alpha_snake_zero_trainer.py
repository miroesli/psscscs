from numpy import array, argmax

from time import time

from utils.agent import Agent
from utils.game import Game
from utils.alphaNNet import AlphaNNet

# https://web.stanford.edu/~surag/posts/alphazero.html


class AlphaSnakeZeroTrainer:
    
    def __init__(self, numIters=5,
                 numEps=2000,
                 competeEps=200,
                 threshold=0.55,
                 height=11,
                 width=11,
                 snake_cnt=8,
                 model=None,
                 **config):

        self.numIters = numIters
        self.numEps = numEps
        self.competeEps = competeEps
        self.threshold = threshold
        self.height = height
        self.width = width
        self.snake_cnt = snake_cnt
        self.model = model

    def train_alpha(self, nnet):
        # for training, all agents uses the same nnet
        # unless we want to use a evolution algorithm
        Alice = Agent(nnet, range(self.snake_cnt), training=True)
        for iter in range(self.numIters):
            X = []
            Y = []
            t0 = time()
            # the loop below can use distributed computing
            for ep in range(self.numEps):
                # collect examples from a new game
                g = Game(self.height, self.width, self.snake_cnt)
                winner_id = g.run(Alice)
                for snake_id in Alice.records:
                    step = len(Alice.records[snake_id])
                    X += Alice.records[snake_id]
                    # assign estimated policies
                    # this substitutes the MCTS
                    gamma = 1
                    if snake_id == winner_id:
                        for j in range(step):
                            move = Alice.moves[snake_id][j]
                            decay = [0] * 4
                            boost = 0
                            for k in range(4):
                                if k != move:
                                    decay[k] = Alice.policies[snake_id][j][k]*gamma
                                    boost += decay[k]
                            for k in range(4):
                                if k == move:
                                    Alice.policies[snake_id][j][k] += boost
                                else:
                                    Alice.policies[snake_id][j][k] -= decay[k]
                            gamma *= 0.8
                    else:
                        for j in range(step):
                            move = Alice.moves[snake_id][j]
                            decay = Alice.policies[snake_id][j][move]*gamma
                            boost = decay/3.0
                            for k in range(4):
                                if k == move:
                                    Alice.policies[snake_id][j][k] -= decay
                                else:
                                    Alice.policies[snake_id][j][k] += boost
                            gamma *= 0.8
                    Y += Alice.policies[snake_id]
                Alice.clear()
            print("Self play time", time() - t0)
            new_nnet = nnet.copy()
            t0 = time()
            new_nnet.train(array(X), array(Y), ep=64, bs=len(X)//2) # bs=len(X)//?
            print("Training time", time() - t0)
            # compare new net with previous net
            t0 = time()
            frac_win = self.compete(new_nnet, nnet)
            if frac_win > self.threshold:
                # replace with new net
                nnet = new_nnet
                print("Iteration", iter, "beats the previouse version with a WR of", frac_win, "\nIt is now the new champion!")
            else:
                print("Iteration", iter, "failed to beat the previouse one. WR =", frac_win)
            print("Competing time", time() - t0, "\n")
        return nnet

    def train(self):
        if self.model:
            nnet = AlphaNNet(model=self.model)
        else:
            nnet = AlphaNNet(in_shape=(self.height*2 - 1, self.width*2 - 1, 1))
        model_num = 0
        while 1:
            new_nnet = self.train_alpha(nnet)
            # need to store the nnet
            if not (nnet is new_nnet):
                nnet = new_nnet
                model_num += 1
                nnet.save("Network_No." + str(model_num))
                print("Network saved.")

    def compete(self, nnet1, nnet2):
        sep = self.snake_cnt//2
        Alice = Agent(nnet1, range(sep))
        Bob = Agent(nnet2, range(sep, self.snake_cnt))
        win = 0
        loss = 0
        for _ in range(self.competeEps):
            g = Game(self.height, self.width, self.snake_cnt)
            winner_id = g.run(Alice, Bob, sep=sep)
            if winner_id is None:
                win += 1
                loss += 1
            elif winner_id < sep:
                win += 1
            else:
                loss += 1
        return win/(win + loss)
