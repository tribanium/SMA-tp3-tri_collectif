#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module to test if the modules environment and agent work properly

@authors: Nathan Etourneau, Paul Flagel
"""
from agent import Agent
from environment import Environment
N = 8
M = 8
NA = 15
NB = 10
N_AGENTS = 4
KPLUS = 0.1
KMINUS = 0.3


def test():
    env = Environment(N, M, NA, NB, N_AGENTS, KPLUS, KMINUS)
    obj_grid = env.object_grid()
    agent_grid = env.agent_grid()

    print("Object grid : \n")
    for arr in obj_grid:
        print(*arr)

    print('\n')

    print("Agent grid : \n")
    for arr in agent_grid:
        print(*arr)

    for round in range(100):
        env.agents[1]["agent"].perception(env)
        env.agents[1]["agent"].action(env)
        if round % 10 == 0:
            print(env.agents[1]["agent"].memory)

    print("Object grid : \n")
    for arr in obj_grid:
        print(*arr)

    print('\n')

    print("Agent grid : \n")
    for arr in agent_grid:
        print(*arr)


if __name__ == '__main__':
    test()
