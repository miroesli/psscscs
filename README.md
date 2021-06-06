*This no longer under development because of outdated/stale code which uses an older version of the battlesnake API. Another version can be viewed [here](https://github.com/Fool-Yang/AlphaSnake-Zero). For other projects like this one see the [awesome-battlesnakes](https://github.com/xtagon/awesome-battlesnake) repository or check out [my profile](https://github.com/miroesli).*

# PSSCSCS

A reinforcement learning [Battlesnake AI](http://battlesnake.com) written in
Python by a **P**hysics, 2 **S**oftware Engineering, and 2 **C**omputer
**S**cience undergrads.

## Presentation

- Google Drive presentation [link](https://drive.google.com/drive/folders/1Knb5xECKhTKK9vVSAutyHNOFClFaFf8o)
- Report [link](https://github.com/Fool-Yang/AlphaSnake-Zero/blob/master/report.pdf)

## Demo

![7000 Iterations DQN Training](./app/gifs/gif-run-7000.gif)
  
## Project specific info  
Currently a 3 layer nn is used for prediction. While 8 layers are derived from the input, AlphaGo is not being utilized, need to do this.  

Visit [https://github.com/BattlesnakeOfficial/community/blob/master/starter-snakes.md](https://github.com/BattlesnakeOfficial/community/blob/master/starter-snakes.md) for API documentation and instructions for running your AI.

This AI client uses the [bottle web framework](http://bottlepy.org/docs/dev/index.html) to serve requests and the [gunicorn web server](http://gunicorn.org/) for running bottle on Heroku. Dependencies are listed in [requirements.txt](requirements.txt).

<!-- [![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy) -->

## Requirements

- a working Python 2.7/3.7 development environment ([getting started guide](http://hackercodex.com/guide/python-development-environment-on-mac-osx/))
- [pip](https://pip.pypa.io/en/latest/installing.html) to install Python dependencies

## Running the Snake Locally

1. [Fork](https://github.com/miroesli/pssscs/fork) (optional) and clone the repo.

Using SSH

```bash
git clone git@github.com:miroesli/pssscs.git
```

Using HTTPS

```bash
git clone https://github.com/miroesli/pssscs.git
```

2. create the virtualenv  

```bash
python -m venv env
source env/bin/activate
```
 
3. Install dependencies using [pip](https://pip.pypa.io/en/latest/installing.html):

```bash
pip install -r requirements.txt
```

4. Run local server:

```bash
cd app
python main.py
```

5. Test your snake by sending a curl to the running snake

```bash
curl -XPOST -H 'Content-Type: application/json' -d '{ "hello": "world"}' http://localhost:8080/start
```

## Running the Engine

Visit
[https://github.com/BattlesnakeOfficial/engine](https://github.com/BattlesnakeOfficial/engine)
for installing the engine to run the AI.

If you have problems running the engine, make sure you have run make install

```bash
make install
```

and built the board

```bash
./build_board.sh
```

If both `./engine dev` and `engine dev` still do not work, build the engine executable locally

```
go build -o engine cmd/engine/main.go
```

Then try running `./engine dev`

## Deploying to Heroku

1. Create a new Heroku app:

```bash
heroku create [APP_NAME]
```

2. Deploy code to Heroku servers:

```bash
git push heroku master
```

3. Open Heroku app in browser:

```bash
heroku open
```

or visit [http://APP_NAME.herokuapp.com](http://APP_NAME.herokuapp.com).

4. View server logs with the `heroku logs` command:

```bash
heroku logs --tail
```

<!-- ## Questions?

Email [hello@battlesnake.com](mailto:hello@battlesnake.com), or tweet [@battlesnakeio](http://twitter.com/battlesnakeio). -->
