#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main module coding the loop

@authors: Nathan Etourneau, Paul Flagel
"""

import random

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from agent import Agent
from environment import Environment

N = 200
M = 290
NA = 750
NB = 750
N_AGENTS = 100
KPLUS = 0.1
KMINUS = 0.3
MEMORY_BUFFER_SIZE = 50
N_ROUNDS = 2000000
ERROR_RATE = 0.


def plot_objects(env, fig, ax):
    ax.clear()

    obj_rows = []
    obj_cols = []
    obj_category = []
    for obj in env.objects.values():
        if obj.position is None:
            continue
        row, col = obj.position

        obj_rows.append(row)
        obj_cols.append(col)
        obj_category.append(obj.category)

    data = pd.DataFrame(
        {"rows": obj_rows, "cols": obj_cols, "category": obj_category})

    ax = sns.scatterplot(x='cols', y='rows', data=data,
                         hue='category', style='category', ec=None)
    ax.set_xlim(-1, env.M)
    ax.set_ylim(-1, env.N)
    plt.show()


def main(N_ROUNDS, N, M, NA, NB, N_AGENTS, KPLUS, KMINUS, MEMORY_BUFFER_SIZE, ERROR_RATE):
    env = Environment(N, M, NA, NB, N_AGENTS, KPLUS, KMINUS,
                      MEMORY_BUFFER_SIZE, ERROR_RATE)

    fig, ax = plt.subplots()

    # Loop
    keys = list(env.agents.keys())

    for round in range(1, N_ROUNDS+1):
        if round % 1000 == 0:
            print(f"Round n°{round}")

        # Shuffle the agents to mimic the fact that the movement is erratic
        random.shuffle(keys)

        for key in keys:
            agent = env.agents[key].agent
            empty_cells = agent.perception(env)
            agent.action(env, empty_cells)

        if (round) % 50000 == 0:
            plot_objects(env, fig, ax)


if __name__ == '__main__':
    main(N_ROUNDS, N, M, NA, NB, N_AGENTS, KPLUS,
         KMINUS, MEMORY_BUFFER_SIZE, ERROR_RATE)
