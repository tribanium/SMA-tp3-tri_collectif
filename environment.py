#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module with a class Environment used to modelize the environment in a
multi-agent system, and a class Object to modelize objects in the environment.

@authors: Nathan Etourneau, Paul Flagel
"""
import numpy as np
import random


class Environment:
    def __init__(self, N, M, na, nb, agents):
        self.N = N
        self.M = M
        make_object_grid(N, M, na, nb)
        make_agent_grid(N, M, agents)

    def make_object_grid(self, N, M, na, nb):
        self.object_grid = [["0" for _ in range(M)] for _ in range(N)]
        self.init_objects(na, nb)

    def init_objects(self, na, nb):
        """Instantiation of multiple objects on the object grid."""

        full_grid = [(row, col) for row in range(self.N) for col in range(self.M)]
        random_positions = random.sample(full_grid, na + nb)
        random_object_category = random.sample(na * "A" + nb * "B")

        for (row, col), category in zip(random_positions, random_object_category):
            self.object_grid[row][col] = category

    def make_agent_grid(self, N, M, agents):
        """As we differentiate agents and objects, we have to create one grid for each."""

        self.agent_grid = [["0" for col in range(M)] for row in range(N)]
        self.init_agents(agents)

    def init_agents(self, agents):
        """Random instantiation of the agents on the agent_grid."""
        full_grid = [(row, col) for row in range(self.N) for col in range(self.M)]
        random_positions = random.sample(full_grid, len(agents))
        self.agents = {}

        for (row, col), agent in zip(agents, random_positions):
            self.object_grid[row][col] = agent
            self.agents.update({agent.key: (row, col)})

    def is_valid_move(self, position, displacement):
        row, col = position
        drow, dcol = displacement

        # We check that the case after the displacement is actually on the grid.
        if row + drow >= self.N or row + drow < 0:
            return False

        if col + dcol >= self.M or col + dcol < 0:
            return False

        # We check if there is an agent where the agent wishes to go
        if self.agent_grid[row + drow][col + dcol] != "0":
            return False

        return True


class Object:
    def __init__(self, object_class, key):
        self.key = key
        self.object_class = object_class
        self.position = None
