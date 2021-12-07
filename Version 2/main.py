#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Main module coding the loop of the multi-agent system. The scenario here is a
grid of dimensions NxM, with a number na of objects of class A, nb of objects
of class B, n_agents agents, and the purpose of the agents is to walk randomly,
and sort the objects with few rules described in Deneubourg, Jean-Louis et al.
“The dynamics of collective sorting robot-like ants and ant-like robots.”

@authors: Nathan Etourneau, Paul Flagel
"""

import random

import matplotlib.pyplot as plt

from environment import Environment
from visualization import update_matplotlib_plot

N = 200
M = 300
NA = 80
NB = 80
NC = 80
N_AGENTS = 25
KPLUS = 0.1
KMINUS = 0.3
MEMORY_BUFFER_SIZE = 15
N_ROUNDS = 2000000
RATIO = 0.75
SIGNAL_RANGE = 1
MAX_PATIENCE = 15


def main(n_rounds, N, M, na, nb, nc, n_agents, kplus, kminus, memory_buffer_size, ratio, signal_range, max_patience):
    env = Environment(N, M, na, nb, nc, n_agents, kplus, kminus,
                      memory_buffer_size, ratio, signal_range, max_patience)
    fig = plt.figure("Collective Sorting")
    ax = fig.add_subplot(111)

    # Loop
    keys = list(env.agents.keys())

    for round in range(1, n_rounds + 1):
        if round % 100 == 0:
            print(f"Round n°{round}")

        # Shuffle the agents to mimic the fact that the movement is erratic
        random.shuffle(keys)

        for key in keys:
            agent = env.agents[key].agent
            empty_cells = agent.perception(env)
            agent.action(env, empty_cells)

        env.update_pheromones()

        if (round) % 50000 == 0:
            update_matplotlib_plot(env, ax)


if __name__ == '__main__':
    main(N_ROUNDS, N, M, NA, NB, NC, N_AGENTS, KPLUS,
         KMINUS, MEMORY_BUFFER_SIZE, RATIO, SIGNAL_RANGE, MAX_PATIENCE)
