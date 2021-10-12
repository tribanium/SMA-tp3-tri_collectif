#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main module coding the loop

@authors: Nathan Etourneau, Paul Flagel
"""

from agent import Agent
from environment import Environment
import random


N = 50
M = 50
NA = 200
NB = 200
N_AGENTS = 20
KPLUS = 0.1
KMINUS = 0.3
N_ROUNDS = 10000000


def main():
    env = Environment(N, M, NA, NB, N_AGENTS, KPLUS, KMINUS)

    # Loop
    agent_keys = list(env.agents.keys())

    for round in range(N_ROUNDS):
        if round % 10000 == 0:
            print(f"Round : {round}")

        # Shuffle the agents to mock the fact that the movement is erratic
        random.shuffle(agent_keys)

        for agent_key in agent_keys:
            agent = env.agents[agent_key]["agent"]
            agent.perception(env)
            agent.action(env)

            # TODO : add data vizualisation ?

    # Final grids visualisation
    obj_grid = env.object_grid()
    agent_grid = env.agent_grid()

    print("Object grid : \n")
    for arr in obj_grid:
        to_print = ''
        for elt in arr:
            if elt == '0':
                elt = ' '
            to_print += elt + ' '
        print(to_print+'\n')

    print('\n')

    print("END")


if __name__ == '__main__':
    main()
