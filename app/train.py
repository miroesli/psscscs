numIters = 100000
numEps = 1000
competeEps = 100
threshold = 0.55
height = 11
width = 11
player_cnt = 8

from game import Game
from agent import Agent

# https://web.stanford.edu/~surag/posts/alphazero.html
def train():
    # initialise neural network
    nnet = NNet()
    # for training, all agents uses the same nnet
    # unless we want to use a evolution algorithm
    agents = [Agent(nnet, training = True) for _ in range(player_cnt)]
    for i in range(numIters):
        for e in range(numEps):
            # collect examples from a new game
            g = Game(height, width, player_cnt)
            winner_id = g.run(agents)
            for agent in agents:
                # return a new trained nnet
                X = agent.records
                # need to get a good loss function
                Y = 0
                new_nnet = nnet.trainNNet(X, Y)
        # compare new net with previous net
        frac_win = compete(new_nnet, nnet)
        if frac_win > threshold:
            # replace with new net
            nnet = new_nnet
    return nnet

def compete(nnet1, nnet2):
    agents = [None] * player_cnt
    sep = player_cnt//2
    for i in range(sep):
        agents[i] = Agent(nnet1)
    for i in range(sep, player_cnt):
        agents[i] = Agent(nnet2)
    wins = 0
    for _ in range(competeEps):
        g = Game(height, width, player_cnt)
        if g.run(agents) < sep:
            wins += 1
    return win/competeEps

if __name__ == '__main__':
    nnet = train()
    # need to store the nnet
