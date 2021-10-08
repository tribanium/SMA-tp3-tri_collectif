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
    def __init__(self, N, M, na, nb, nb_agents):
        self.N = N
        self.M = M
        self.na = na
        self.nb = nb
        self.nb_agents = nb_agents
        make_object_grid()
        init_agents(nb_agents)

    def make_object_grid(self):
        self.object_grid = [["0" for _ in range(self.M)] for _ in range(self.N)]
        self.init_objects()

    def init_objects(self):
        """Instantiation of multiple objects on the object grid."""

        full_grid = [(row, col) for row in range(self.N) for col in range(self.M)]
        random_positions = random.sample(full_grid, self.na + self.nb)
        random_object_category = random.sample(self.na * "A" + self.nb * "B")

        for (row, col), category in zip(random_positions, random_object_category):
            self.object_grid[row][col] = category


    def init_agents(self):
        """Random instantiation of the agents on the agent_grid."""
        full_grid = [(row, col) for row in range(self.N) for col in range(self.M)]
        random_positions = random.sample(full_grid, self.nb_agents)


        self.agents = {key:(row,col) for key, (row, col) in zip(range(self.nb_agents), random_positions)}

    def is_valid_move(self, key, displacement):
        row, col = self.agents[key]
        drow, dcol = displacement

        # We check that the case after the displacement is actually on the grid.
        if row + drow >= self.N or row + drow < 0:
            return False

        if col + dcol >= self.M or col + dcol < 0:
            return False

        # We check if there is an agent where the agent wishes to go
        if any(row + drow == agent_row and col + dcol == agent_col \
            for (agent_row, agent_col) in self.agents.values()):
            return False

        return True


    def move_object(self, key, displacement):
        pass


    def move_agent(self, key, displacement):
        pass

    def agent_grid(self):
        _agent_grid = [["0" for _ in range(self.M)] for _ in range(self.N)]

        for key, (row, col) in self.agents.items():
            _agent_grid[row][col] = key

        return _agent_grid


class Object:
    def __init__(self, object_class, key):
        self.key = key
        self.object_class = object_class
        self.position = None
