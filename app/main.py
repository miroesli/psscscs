import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response
from utils.data_to_state import translate
from utils.alphaNNet import AlphaNNet
from utils.agent import Agent

DEFAULT_MODEL_CONFIG_PATH = "./settings/default"


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
    #print(json.dumps(data))

    directions = ['up', 'down', 'left', 'right']
    #direction = random.choice(directions)
   
    #TODO: add agent moves if training 

    return {
        'move': directions[snake.make_move(translate(data)[0])],
        'shout': 'import time;print("\U0001F635");time.sleep(10);'
    }
    #return move_response(direction)


@bottle.post('/end')
def end():
    data = bottle.request.json
    #if t:
    #    X = snake.records #will need to create per agent
    #    Y = snake.policies
    #    model.train(list(X), list(Y))
    #snake.clear()
    model.save(config['model'])
    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    print(json.dumps(data))

    return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

#This config file should contain the saved/desired model name, and additional parameters
with open(DEFAULT_MODEL_CONFIG_PATH+".json", "r") as config_file:
    config = json.load(config_file)

model = AlphaNNet(config=config, in_shape=[15, 15])
t = True if config['train'] == 'True' else False #this would be if we want to train via this api also
snake = Agent(nnet=model, training=t)

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
