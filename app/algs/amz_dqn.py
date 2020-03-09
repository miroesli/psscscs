from utils.dqn_agent import Agent
import gym


import argparse
import os
import json

from gym_battlesnake.envs.bs_env import BsEnv
# from mxboard import SummaryWriter

from utils.amz_agent import MultiAgentsCollection

import random
import mxnet as mx
import numpy as np
from collections import deque
from array2gif import write_gif


VERBOSE = True


class DQN:
    def __init__(self,
                 seeds=[0, 666, 15],
                 map_size=[15, 15],
                 number_of_snakes=4,
                 snake_representation='bordered-51s',
                 state_type='one_versus_all',
                 buffer_size=5000,
                 update_every=20,
                 lr_start=0.0005,
                 lr_step=5e5,
                 lr_factor=0.5,
                 gamma=0.95,
                 tau=1e-3,
                 batch_size=64,
                 episodes=100000,
                 max_t=1000,
                 eps_start=1.0,
                 eps_end=0.01,
                 eps_decay=0.995,
                 warmup=0,
                 load=None,
                 load_only_conv_layers=False,
                 qnetwork_type='attention',
                 starting_channels=6,
                 number_of_conv_layers=3,
                 number_of_dense_layers=2,
                 depthS=10,
                 depth=200,
                 number_of_hidden_states=128,
                 kernel_size=3,
                 repeat_size=3,
                 activation_type='softrelu',
                 sequence_length=2,
                 print_score_steps=100,
                 models_to_save='all',
                 save_only_best_models=False,
                 save_model_every=2000,
                 model_dir='models',
                 render_steps=1000,
                 should_render='store_true',
                 writer='store_true',
                 print_progress='store_true',
                 run_name='run',
                 **config):
        self.seeds = list(seeds)
        self.map_size = map_size
        self.number_of_snakes = number_of_snakes
        self.snake_representation = snake_representation
        self.state_type = state_type
        self.buffer_size = buffer_size
        self.update_every = update_every
        self.lr_start = lr_start
        self.lr_step = lr_step
        self.lr_factor = lr_factor
        self.gamma = gamma
        self.tau = tau
        self.batch_size = batch_size
        self.episodes = episodes
        self.max_t = max_t
        self.eps_start = eps_start
        self.eps_end = eps_end
        self.eps_decay = eps_decay
        self.warmup = warmup
        self.load = load
        self.load_only_conv_layers = load_only_conv_layers
        self.qnetwork_type = qnetwork_type
        self.starting_channels = starting_channels
        self.number_of_conv_layers = number_of_conv_layers
        self.number_of_dense_layers = number_of_dense_layers
        self.depthS = depthS
        self.depth = depth
        self.number_of_hidden_states = number_of_hidden_states
        self.kernel_size = kernel_size
        self.repeat_size = repeat_size
        self.activation_type = activation_type
        self.sequence_length = sequence_length
        self.print_score_steps = print_score_steps
        self.models_to_save = models_to_save
        self.save_only_best_models = save_only_best_models
        self.save_model_every = save_model_every
        self.model_dir = model_dir
        self.render_steps = render_steps
        self.should_render = should_render
        self.writer = writer
        self.print_progress = print_progress
        self.run_name = run_name

    def train(self):
        for seed in self.seeds:
            # if self.writer:
            #     writer = SummaryWriter(
            #         "logs/{}-seed{}".format(run_name, seed), verbose=False)
            # else:
            #     writer = None

            # Initialise the environment
            self.env = BsEnv(
                map_size=self.map_size, observation_type=self.snake_representation)
            self.env.seed(seed)

            # Initialise agent
            if self.state_type == "layered":
                state_depth = 1+self.number_of_snakes
            elif self.state_type == "one_versus_all":
                state_depth = 3

            if "bordered" in self.snake_representation:
                state_shape = (
                    self.map_size[0]+2, self.map_size[1]+2, state_depth)
            else:
                state_shape = (map_size[0], map_size[1], state_depth)

            agent_params = (seed, self.model_dir,
                            self.load, self.load_only_conv_layers,
                            self.models_to_save,
                            # State configurations
                            self.state_type, state_shape, self.number_of_snakes,

                            # Learning configurations
                            self.buffer_size, self.update_every,
                            self.lr_start, self.lr_step, self.lr_factor,
                            self.gamma, self.tau, self.batch_size,

                            # Network configurations
                            self.qnetwork_type, self.sequence_length,
                            self.starting_channels, self.number_of_conv_layers,
                            self.number_of_dense_layers, self.number_of_hidden_states,
                            self.depthS, self.depth,
                            self.kernel_size, self.repeat_size,
                            self.activation_type)

            self.agents = MultiAgentsCollection(*agent_params)
            self.dqn_run()

    def dqn_run(self):
        """Deep Q-Learning.

        Inspired from torch code provided in 
        https://github.com/udacity/deep-reinforcement-learning/blob/master/dqn/solution/Deep_Q_Network_Solution.ipynb
        """
        scores = [[] for _ in range(self.number_of_snakes)]
        scores_window = [deque(maxlen=100)
                         for _ in range(self.number_of_snakes)]
        timesteps = deque(maxlen=100)

        eps = self.eps_start
        max_time_steps = 0

        for i_episode in range(1, self.episodes+1):
            state, _, dones, info = self.env.reset()
            info["episodes"] = i_episode
            score = [0 for _ in range(self.number_of_snakes)]
            rgb_arrays = []
            self.agents.reset()
            for t in range(self.max_t):

                actions = self.agents.get_actions(state, dones, info, t, eps)
                next_state, reward, dones, info = self.env.step(actions)
                info["episodes"] = i_episode

                if i_episode > self.warmup:
                    should_learn = True
                else:
                    should_learn = False

                self.agents.step(state, actions, reward, next_state, dones, info, t,
                                 should_learn)
                for i in range(self.number_of_snakes):
                    score[i] += reward[i]

                state = next_state
                if self.should_render and (i_episode % self.render_steps == 0):
                    rgb_array = self.env.render(mode="rgb_array")
                    rgb_arrays.append(rgb_array)

                number_of_snakes_alive = sum(list(dones.values()))
                if self.number_of_snakes - number_of_snakes_alive <= 1:
                    break

            if self.should_render and (i_episode % self.render_steps == 0):
                write_gif(rgb_arrays, 'gifs/gif:{}-{}.gif'.format(self.run_name, i_episode),
                          fps=5)

            timesteps.append(self.env.turn_count)
            for i in range(self.number_of_snakes):
                scores_window[i].append(score[i])
                scores[i].append(score[i])

            eps = max(self.eps_end, self.eps_decay*eps)
            # if self.writer:
            #     for i in range(self.number_of_snakes):
            #         self.writer.add_scalar("rewards_{}".format(i),
            #                                score[i], i_episode)
            #     self.writer.add_scalar("max_timesteps", t, i_episode)

            average_score = ""
            for i in range(self.number_of_snakes):
                score_window = scores_window[i]
                average_score += "\t{:.2f}".format(np.mean(score_window))

            print_string = 'Episode {}\tAverage Score: {}\tMean timesteps {:.2f}'.format(
                i_episode, average_score, np.mean(timesteps))
            if self.print_progress:
                print("\r"+print_string, end="")
            if i_episode % self.print_score_steps == 0:
                if self.print_progress:
                    print("\r"+print_string)
                else:
                    print(print_string)

            if self.save_only_best_models:
                if self.env.turn_count > max_time_steps:
                    if i_episode % self.save_model_every == 0 and i_episode > 200:
                        max_time_steps = self.env.turn_count
                        self.agents.save(self.run_name, i_episode)
            else:
                if i_episode % self.save_model_every == 0:
                    self.agents.save(self.run_name, i_episode)
