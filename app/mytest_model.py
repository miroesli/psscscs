from utils.alphaNNet import AlphaNNet
from utils.agent import Agent
from utils.mytest_game import Game
from player import Player

#file_name = input("\nEnter the model file name:\n")
file_name = 'Network_No.15.h5'
net = AlphaNNet(model = file_name)
snake_cnt = 4 #int(input("Enter the number of snakes:\n"))

f = open("replay.txt", 'w')
f.write('')
f.close()

for _ in range(3):
    g = Game(11, 11, snake_cnt)
    g.run(Agent(net, list(range(snake_cnt))))

Player().main()
