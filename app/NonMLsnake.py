import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
from data_to_state import translate

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    print(json.dumps(data))

    # See https://docs.battlesnake.com/snake-customization for customizations

    color = '#00FFFF'
    headType = 'bwc-scarf'
    tailType = 'freckled'

    return start_response(color, headType, tailType)


@bottle.post('/move')
def move():
    data = bottle.request.json

    """
    TODO: Using the data from the endpoint request object, your
            snake AI must choose a direction to move in.
    """
    print(json.dumps(data))

    state = translate(data)
    
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
    
    directions = ['up', 'down', 'left', 'right']
    direction = directions[ds.index(min(ds))]

    return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
