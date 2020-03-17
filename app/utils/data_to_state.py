from numpy import array
max_snakes = 8
EMPTY = 0.5
# adders & mutipliers
# (value + value_a) * value_m
HUNGER_a = -101
HUNGER_m = 0.01
SNAKE_m = 0.02
HEAD_m = 0.04
WALL = 1.0

def make_state(you, snakes, food, shape=[11,11]):
        """ Process the data and translate them into a grid
        
        Args:
            you: a Snake object define by snake.py; represents this snake
        
        Return:
            grid: a grid that represents the game
        
        """
        print(you)
        # gotta do the math to recenter the grid
        width = shape[0] * 2 - 1
        height = shape[1] * 2 - 1
        grid = [[[0.0, WALL, 0.0] for col in range(width)] for row in range(height)]
        center_y = height//2
        center_x = width//2
        # the original game board
        # it's easier to work on the original board then transfer it onto the grid
        board = [[[0.0, 0.0, 0.0] for col in range(shape[0])] for row in range(shape[1])]

        # positions are (y, x) not (x, y)
        # because you read the grid row by row, i.e. (row number, column number)
        # otherwise the board is transposed
        length_minus_half = len(you['body']) - 0.5
        for snake in snakes:
            print(snake['body'])
            body = snake['body']
            # get head
            board[body[0]['y']][body[0]['x']][0] = (len(body) - (length_minus_half)) * HEAD_m
            # get the rest of the body
            dist = 1
            for i in range(len(body)-1, 0, -1):
                board[body[i]['y']][body[i]['x']][1] = dist * SNAKE_m
                dist += 1

        #for food in food:
        #    board[food[0]][food[1]][2] = (101 - you['health']) * HUNGER_m

        # get my head
        head_y = you['body'][0]['y']
        head_x = you['body'][0]['x']
        board[head_y][head_x] = [1.0 - int(you['health'])/100.0] * 3

        # from this point, all positions are measured relative to our head
        for y in range(shape[1]):
            for x in range(shape[0]):
                grid[y - head_y + center_y][x - head_x + center_x] = board[y][x]

        return grid

def translate(data):
    """ Preprocess the data

    Args:
        data: the data defined by the
                Battlesnake Snake API (2020.01)
                https://docs.battlesnake.com/snake-api

    Return:
        state: the game state defined by game.py

    """

    height = data['board']['height']
    width = data['board']['width']

    state = array([[[EMPTY] * width for row in range(height)]
                   for layer in range(max_snakes)])

    health = data['you']['health']
    dist = len(data['you']['body'])
    for b in data['you']['body']:
        state[0][b['y']][b['x']] = EMPTY + dist * SNAKE_m
        dist -= 1
    for food in data['board']['food']:
        state[0][food['y']][food['x']] = EMPTY + (health + HUNGER_a) * HUNGER_m

    i = 1
    for snake in data['board']['snakes']:
        health = snake['health']
        dist = len(snake['body'])
        for b in snake['body']:
            try:
                state[i][b['y']][b['x']] = EMPTY + dist * SNAKE_m
            except IndexError:
                print(len(data['board']['snakes']), i, b)
                print("\n\n\n\n\n\n")
            dist -= 1
        for food in data['board']['food']:
            state[i][food['y']][food['x']] = EMPTY + \
                (health + HUNGER_a) * HUNGER_m
        i += 1

    # , (data['you']['body'][0]['y'], data['you']['body'][0]['x'])
    return state
