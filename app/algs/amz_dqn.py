from utils.dqn_agent import Agent
import gym


import argparse
import os
import json

from gym_battlesnake.snake_gym import bs_env
from mxboard import SummaryWriter

from utils.amz_agent import MultiAgentsCollection

import random
import mxnet as mx
import numpy as np
from collections import deque
from array2gif import write_gif


VERBOSE = True


class DQN:
    def __init__(self, iterations=100,
                 seeds=[0, 666, 15],
                 map_size=[15, 15],
                 number_of_snakes=4,
                 snake_representation='bordered-51s',
                 state_type='one_vs_all',
                 environment='gym_battlesnake:bs-v0',
                 **config):
        # Initialise the environment
        env = BattlesnakeGym(
            map_size=map_size, observation_type=args.snake_representation)
        env.seed(seed)

        # Initialise agent
        if args.state_type == "layered":
            state_depth = 1+args.number_of_snakes
        elif args.state_type == "one_versus_all":
            state_depth = 3

        if "bordered" in args.snake_representation:
            state_shape = (map_size[0]+2, map_size[1]+2, state_depth)
        else:
            state_shape = (map_size[0], map_size[1], state_depth)

        agent_params = (seed, model_dir,
                        load, args.load_only_conv_layers,
                        args.models_to_save,
                        # State configurations
                        args.state_type, state_shape, args.number_of_snakes,

                        # Learning configurations
                        args.buffer_size, args.update_every,
                        args.lr_start, args.lr_step, args.lr_factor,
                        args.gamma, args.tau, args.batch_size,

                        # Network configurations
                        args.qnetwork_type, args.sequence_length,
                        args.starting_channels, args.number_of_conv_layers,
                        args.number_of_dense_layers, args.number_of_hidden_states,
                        args.depthS, args.depth,
                        args.kernel_size, args.repeat_size,
                        args.activation_type)

        agent = MultiAgentsCollection(*agent_params)

        trainer(env, agent, args.number_of_snakes,
                args.run_name, args.episodes,
                args.max_t, args.warmup,
                args.eps_start, args.eps_end, args.eps_decay,

                args.print_score_steps,
                args.save_only_best_models,
                args.save_model_every,
                args.render_steps, args.should_render,
                args.writer, args.print_progress)

    def train(self):
        """Deep Q-Learning.

        Inspired from torch code provided in 
        https://github.com/udacity/deep-reinforcement-learning/blob/master/dqn/solution/Deep_Q_Network_Solution.ipynb
        """
        scores = [[] for _ in range(number_of_snakes)]
        scores_window = [deque(maxlen=100) for _ in range(number_of_snakes)]
        timesteps = deque(maxlen=100)

        eps = eps_start
        max_time_steps = 0

        for i_episode in range(1, n_episodes+1):
            state, _, dones, info = env.reset()
            info["episodes"] = i_episode
            score = [0 for _ in range(number_of_snakes)]
            rgb_arrays = []
            agents.reset()
            for t in range(max_t):

                actions = agents.get_actions(state, dones, info, t, eps)
                next_state, reward, dones, info = env.step(actions)
                info["episodes"] = i_episode

                if i_episode > warmup:
                    should_learn = True
                else:
                    should_learn = False

                agents.step(state, actions, reward, next_state, dones, info, t,
                            should_learn)
                for i in range(number_of_snakes):
                    score[i] += reward[i]

                state = next_state
                if should_render and (i_episode % render_steps == 0):
                    rgb_array = env.render(mode="rgb_array")
                    rgb_arrays.append(rgb_array)

                number_of_snakes_alive = sum(list(dones.values()))
                if number_of_snakes - number_of_snakes_alive <= 1:
                    break

            if should_render and (i_episode % render_steps == 0):
                write_gif(rgb_arrays, 'gifs/gif:{}-{}.gif'.format(name, i_episode),
                          fps=5)

            timesteps.append(env.turn_count)
            for i in range(number_of_snakes):
                scores_window[i].append(score[i])
                scores[i].append(score[i])

            eps = max(eps_end, eps_decay*eps)
            if writer:
                for i in range(number_of_snakes):
                    writer.add_scalar("rewards_{}".format(i),
                                      score[i], i_episode)
                writer.add_scalar("max_timesteps", t, i_episode)

            average_score = ""
            for i in range(number_of_snakes):
                score_window = scores_window[i]
                average_score += "\t{:.2f}".format(np.mean(score_window))

            print_string = 'Episode {}\tAverage Score: {}\tMean timesteps {:.2f}'.format(
                i_episode, average_score, np.mean(timesteps))
            if print_progress:
                print("\r"+print_string, end="")
            if i_episode % print_score_steps == 0:
                if print_progress:
                    print("\r"+print_string)
                else:
                    print(print_string)

            if save_only_best_models:
                if env.turn_count > max_time_steps:
                    if i_episode % save_model_every == 0 and i_episode > 200:
                        max_time_steps = env.turn_count
                        agents.save(name, i_episode)
            else:
                if i_episode % save_model_every == 0:
                    agents.save(name, i_episode)
