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

N = 50
M = 50
NA = 200
NB = 200
N_AGENTS = 20
KPLUS = 0.1
KMINUS = 0.3
MEMORY_BUFFER_SIZE = 10
N_ROUNDS = 2000000


def plot_objects(env, fig, ax):
    obj_rows = []
    obj_cols = []
    obj_category = []
    for obj in env.objects.values():
        row, col = obj.position

        obj_rows.append(row)
        obj_cols.append(col)
        obj_category.append(obj.category)

    data = pd.DataFrame(
        {"rows": obj_rows, "cols": obj_cols, "category": obj_category})

    ax.clear()

    ax = sns.scatterplot(x='rows', y='cols', data=data,
                         hue='category', style='category', ec=None)
    ax.set_xlim(0, env.M)
    ax.set_ylim(0, env.N)
    plt.show()


def main():
    env = Environment(N, M, NA, NB, N_AGENTS, KPLUS,
                      KMINUS, MEMORY_BUFFER_SIZE)

    fig, ax = plt.subplots()

    # Loop
    agent_keys = list(env.agents.keys())

    for round in range(N_ROUNDS):

        # Shuffle the agents to mimic the fact that the movement is erratic
        random.shuffle(agent_keys)

        for key in agent_keys:
            agent = env.agents[key].agent
            agent.perception(env)
            agent.action(env)

        if (round + 1) % 30000 == 0:
            plot_objects(env, fig, ax)
            print(f"Round n°{round+1}")

    print("END")


if __name__ == '__main__':
    main()
