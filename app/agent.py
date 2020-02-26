from preprocess import preprocess

class Agent:
    
    def make_move(self, game, snake):
        grid = preprocess(game, snake)
        # (y, x) i.e. (row number, column number)
        center = (len(grid[0])//2, len(grid)//2)
        values = [
            grid[center[1] - 1][center[0]], # 0 = up
            grid[center[1] + 1][center[0]], # 1 = down
            grid[center[1]][center[0] - 1], # 2 = left
            grid[center[1]][center[0] + 1]  # 3 = right
        ]
        return values.index(min(values))
