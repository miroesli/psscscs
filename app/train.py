import json
import os
import sys

DEFAULT_TRAIN_CONFIG_PATH = "../settings/train_params"
DEFAULT_ALGS_PATH = "../algs/"


def train():
    pass


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
        trial = sys.argv[1]

    try:
        algorithm = config[trial]['algorithm']
        iterations = config[trial]['iterations']
    except Exception:
        print("Missing training parameter")
        exit(0)

    # if os.path.exists(DEFAULT_ALGS_PATH+"/"+algorithm):
    #     os.system("python "+model_path+" "+data_dir_path+" "+results_dir_path)

    # use them as classes?

    # check if alg = nn or other and run the associated algorithm

    # compare its performance with the previous


if __name__ == "__main__":
    main()
