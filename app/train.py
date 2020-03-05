import json
import sys
# import os

from algs import *

# from algs.neuralnet import Neuralnet
# from algs.template import Template

DEFAULT_TRAIN_CONFIG_PATH = "./settings/train_params"
DEFAULT_ALGS_PATH = "./algs/"
VERBOSE = True


def usage():
    print("Usage: python train.py [path/to/config/file] trial_name")


def main():
    # check if there is an input file
    if len(sys.argv) > 3 or len(sys.argv) < 2:
        print("Incorrect usage...")
        usage()
        exit(0)

    if len(sys.argv) == 3:
        # parse the input json file and run the associated training alg
        try:
            with open(sys.argv[1]+".json", "r") as config_file:
                config = json.load(config_file)
        except FileNotFoundError:
            print("No configuration file found. Using default.")
        with open(DEFAULT_TRAIN_CONFIG_PATH+".json", "r") as config_file:
            config = json.load(config_file)
        trial = sys.argv[2]
    else:
        with open(DEFAULT_TRAIN_CONFIG_PATH+".json", "r") as config_file:
            config = json.load(config_file)
        trial = sys.argv[1]

    if VERBOSE:
        config = config[trial]

    try:
        algorithm = config['algorithm']
    except Exception:
        print("Missing algorithm parameter")
        exit(0)

    print(dict(**config))

    if algorithm == 'neuralnet':
        alg = neuralnet(**config)
    else:
        alg = template(**config)

    alg.train()

    # TODO: store the trained model in models folder


if __name__ == "__main__":
    main()
