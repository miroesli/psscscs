from numpy import array
max_snakes = 8
EMPTY = 0.5
# adders & mutipliers
# (value + value_a) * value_m
HUNGER_a = -101
SNAKE_m = 0.02
WALL = 1.0
HEAD_m = 0.04
HUNGER_m = 0.01
def translate(data):
    """ Preprocess the data

    Args:
        data: the data defined by the
                Battlesnake Snake API (2020.01)
                https://docs.battlesnake.com/snake-api

    Return:
        state: the game state defined by game.py

    Note:
        The resulting state consists of 3 layers: one for food, obstacles, and other snakes
        so output state is 21x21x3

    """



    height = data['board']['height']
    width = data['board']['width']

    height = height * 2 - 1
    width = width * 2 - 1

    grid = [[[0.0, WALL, 0.0] for col in range(width)] for row in range(height)]
    center_y = height//2
    center_x = width//2
    # the original game board
    # it's easier to work on the original board then transfer it onto the grid
    board = [[[0.0, 0.0, 0.0] for col in range(data['board']['width'])] for row in range(data['board']['height'])]

    # positions are (y, x) not (x, y)
    # because you read the grid row by row, i.e. (row number, column number)
    # otherwise the board is transposed
    length_minus_half = len(data['you']['body']) - 0.5
    for snake in data['board']['snakes']:
        body = snake['body']
        # get head
        board[body[0]['y']][body[0]['x']][0] = (len(body) - (length_minus_half)) * HEAD_m
        # get the rest of the body
        dist = 1
        for i in range(len(body)-1, 0, -1):
            board[body[i]['y']][body[i]['x']][1] = dist * SNAKE_m
            dist += 1

    for food in data['board']['food']:
        board[food['y']][food['x']][2] = (101 - data['you']['health']) * HUNGER_m

    # get my head
    head_y, head_x = data['you']['body'][0]
    board[head_y][head_x] = [1.0 - data['you']['health']/100.0] * 3

    # from this point, all positions are measured relative to our head
    for y in range(data['board']['height']):
        for x in range(data['board']['height']):
            grid[y - head_y + center_y][x - head_x + center_x] = board[y][x]

    return grid 

