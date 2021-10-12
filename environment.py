#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module with a class Environment used to modelize the environment in a
multi-agent system, and a class Object to modelize objects in the environment.

@authors: Nathan Etourneau, Paul Flagel
"""
import numpy as np
import random

from agent import Agent


class Environment:
    def __init__(self, N, M, na, nb, n_agents, kplus, kminus):
        self.N = N
        self.M = M
        self.na = na
        self.nb = nb

        self.n_agents = n_agents
        self.kplus = kplus
        self.kminus = kminus

        self.init_objects()
        self.init_agents()

    def init_objects(self):
        """Instanciation of na objects of category A and nb objects of category B at
        na + nb random positions on the gridL"""

        full_grid = [(row, col) for row in range(self.N)
                     for col in range(self.M)]
        random_positions = random.sample(full_grid, self.na + self.nb)
        random_object_category = random.sample(
            self.na * "A" + self.nb * "B", self.na + self.nb)

        self.objects = {}

        for key, (category, position) in enumerate(zip(random_object_category, random_positions), 1):
            self.objects[key] = Object(key, category, position)

    def init_agents(self):
        """Initialisation of the positions of the n_agents agents on the grid
        at n_agents random positions."""
        full_grid = [(row, col) for row in range(self.N)
                     for col in range(self.M)]
        random_positions = random.sample(full_grid, self.n_agents)

        self.agents = {}
        for key, (row, col) in enumerate(random_positions, 1):
            self.agents[key] = {"position": (
                row, col), "agent": Agent(key, self.kplus, self.kminus)}

    def is_valid_agent_move(self, key, displacement):
        """Checks if a specified displacement is valid for an agent : there can
        only be one object per case, and the displacement must not make the
        object go out of the grid"""
        if displacement == (0, 0):
            return True

        row, col = self.agents[key]["position"]
        drow, dcol = displacement

        # We check that the case after the displacement is actually on the grid.
        if row + drow >= self.N or row + drow < 0:
            return False

        if col + dcol >= self.M or col + dcol < 0:
            return False

        # We check if there is an agent where the agent wishes to go
        for agent_dict in self.agents.values():
            agent_row, agent_col = agent_dict["position"]
            if (row + drow, col + dcol) == (agent_row, agent_col):
                return False

        return True

    def is_valid_object_move(self, key, displacement):
        """Checks if a specified displacement is valid for an object : there
        can only be one object per case, and the displacement must not make the
        object go out of the grid"""
        if displacement == (0, 0):
            return True

        row, col = self.objects[key].position
        drow, dcol = displacement

        # We check that the case after the displacement is actually on the grid.
        if row + drow >= self.N or row + drow < 0:
            return False

        if col + dcol >= self.M or col + dcol < 0:
            return False

        # We check if there is an agent where the agent wishes to go
        for obj in self.objects.values():
            obj_row, obj_col = obj.position

            if row + drow == obj_row and col + dcol == obj_col:
                return False
        return True

    def move_object(self, key, displacement):
        """Moves the object of a specified displacement"""
        if displacement == (0, 0):
            return

        drow, dcol = displacement
        row, col = self.objects[key].position
        self.objects[key].position = (row+drow, col+dcol)

    def move_agent(self, key, displacement):
        """Moves the agent of a specified displacement"""
        if displacement == (0, 0):
            return

        drow, dcol = displacement
        row, col = self.agents[key]["position"]
        self.agents[key]["position"] = (row+drow, col+dcol)

    def agent_grid(self):
        """Returns a grid showing where the agents are"""
        _agent_grid = [["0" for _ in range(self.M)] for _ in range(self.N)]

        for key, agent_dict in self.agents.items():
            row, col = agent_dict["position"]
            _agent_grid[row][col] = key

        return _agent_grid

    def object_grid(self):
        """Returns a grid showing where the objects are"""
        _object_grid = [["0" for _ in range(self.M)] for _ in range(self.N)]

        for obj in self.objects.values():
            row, col = obj.position
            _object_grid[row][col] = obj.object_category

        return _object_grid

    def get_case_data(self, key):
        """Checks if the agent with the specified key is on a case with an
        object, and if this is the case, return the category of the object and
        its key"""
        position = self.agents[key]["position"]

        for obj in self.objects.values():
            if obj.position == position:
                return obj.object_category, obj.key
        return "0", None


class Object:
    def __init__(self, key, object_category, position):
        self.key = key
        self.object_category = object_category
        self.position = position
