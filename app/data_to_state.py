EMPTY = 0.5
WALL = 1.0
MYHEAD = -1.0
# adders & mutipliers
# (value + value_a) * value_m
HUNGER_a = -100
HUNGER_m = 0.005
SNAKE_m = 0.01

def preprocess(data):
    """ Preprocess the data
    
    Args:
        data: the data defined by the
                Battlesnake Snake API (2020.01)
                https://docs.battlesnake.com/snake-api
    
    Return:
        grid: A grid that represents the game
    
    """
    
    # gotta do the math to recenter the grid
    width = (data['board']['width'] + 1) * 2 - 1
    height = (data['board']['height'] + 1) * 2 - 1
    grid = [[WALL] * width for row in range(height)]
    center = (width//2, height//2)
    # the original game board
    # it's easier to work on the original board then transfer it onto the grid
    board = [[EMPTY] * data['board']['width'] for row in range(data['board']['height'])]
    
    # positions are (y, x) not (x, y)
    # because you read the grid row by row, i.e. (row number, column number)
    # otherwise the board is transposed
    for food in data['board']['food']:
        # I suppose a food is more wanted than an enmpty cell so let EMPTY be the base value
        board[food['y']][food['x']] += (data['you']['health'] + HUNGER_a) * HUNGER_m
    
    my_length = len(data['you']['body'])
    for snake in data['board']['snakes']:
        body = snake['body']
        # get head
        board[body[0]['y']][body[0]['x']] = EMPTY + (len(body) - (my_length - 1)) * SNAKE_m
        # get the rest of the body
        dist = len(body)
        # Don't do the body[1:] slicing. It will copy the list
        for i in range(1, len(body)):
            board[body[i]['y']][body[i]['x']] = EMPTY + dist * SNAKE_m
            dist -= 1
    
    body = data['you']['body']
    # get head
    board[body[0]['y']][body[0]['x']] = MYHEAD
    # get the rest of the body
    dist = my_length
    for i in range(1, len(body)):
        board[body[i]['y']][body[i]['x']] = EMPTY + dist * SNAKE_m
        dist -= 1
    
    if data['you']['name'] == 'test_board' or data['you']['name'] == 'test':
        print()
        for row in board:
            print(row)
        print()
    
    # from this point, all positions are measured relative to our head
    origin = data['you']['body'][0]
    for y in range(data['board']['height']):
        for x in range(data['board']['width']):
            grid[y - origin['y'] + center[1]][x - origin['x'] + center[0]] = board[y][x]
    
    if data['you']['name'] == 'test_grid'or data['you']['name'] == 'test':
        print()
        for row in grid:
            print(row)
        print()
    
    return grid
