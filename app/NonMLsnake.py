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
    
    y = data['you']['body'][0]['y']
    x = data['you']['body'][0]['x']
    
    state = translate(data)
    
    ds = [0] * 4

    if y > 0:
        for board in state:
            ds[0] += board[y - 1][x]
    else:
        ds[0] = 1000
    if y < len(state[0]) - 1:
        for board in state:
            ds[1] += board[y + 1][x]
    else:
        ds[1] = 1000
    if x > 0:
        for board in state:
            ds[2] += board[y][x - 1]
    else:
        ds[2] = 1000
    if x < len(state[0][0]) - 1:
        for board in state:
            ds[3] += board[y][x + 1]
    else:
        ds[3] = 1000
    
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
