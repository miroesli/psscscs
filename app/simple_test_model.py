from utils.alphaNNet import AlphaNNet
from utils.agent import Agent
from utils.game import Game
net = AlphaNNet(model = "Network_No.24")
agents = [Agent(net, training = False) for _ in range(8)]
g = Game(11, 11, 8)
g.run(agents)