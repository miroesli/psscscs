import random
from time import time

from game import Game

class nonMLagent:

    def make_move(self, state):
        _max = -1
        for _y in range(len(state)):
            for _x in range(len(state[0])):
                if _max < state[0][_y][_x]:
                    _max = state[0][_y][_x]
                    y = _y
                    x = _x
        ds = [0] * 4
        for board in state:
            if y > 0:
                ds[0] += board[y - 1][x]
            else:
                ds[0] = 100
            if y < len(state) - 1:
                ds[1] += board[y + 1][x]
            else:
                ds[1] = 100
            if x > 0:
                ds[2] += board[y][x - 1]
            else:
                ds[2] = 100
            if x < len(state[0]) - 1:
                ds[3] += board[y][x + 1]
            else:
                ds[3] = 100
        return ds.index(min(ds))

'''
for it is easy for a human to read,
I have swithed on the state printing in game.py
run this file with command python run_this_test_and_output_to_a_file.py > output.txt
see if the results make sense

a 1-8 number represents a snake body, with value = its id

9 represents a food

feel free to make your own test
'''

agents = [nonMLagent()] * 8
t0 = time()
for _ in range(100):
    g = Game(11, 11, 8)
    g.run(agents)
print("totoal run time ", time() - t0)
