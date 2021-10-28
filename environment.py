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
    def __init__(self, N, M, na, nb, n_agents, kplus, kminus, memory_buffer_size=15, error_rate=0.):
        self.N = N
        self.M = M

        self.grid = [[Cell(position=(row, col))
                      for col in range(M)] for row in range(N)]
        self.init_grid(na, nb, n_agents, kplus, kminus,
                       memory_buffer_size, error_rate)

    def init_grid(self, na, nb, n_agents, kplus, kminus, memory_buffer_size, error_rate):
        self.init_objects(na, nb)
        self.init_agents(n_agents, kplus, kminus,
                         memory_buffer_size, error_rate)

        for obj in self.objects.values():
            row, col = obj.position
            self.grid[row][col].object = obj

        for agent_data in self.agents.values():
            row, col = agent_data.position
            self.grid[row][col].agent = agent_data.agent

    def init_objects(self, na, nb):
        """Instanciation of na objects of category A and nb objects of category B at
        na + nb random positions on the grid"""

        grid = [(row, col) for row in range(self.N)
                for col in range(self.M)]
        random_positions = random.sample(grid, na + nb)
        random_object_category = random.sample(
            na * "A" + nb * "B", na + nb)

        self.objects = {}

        for key, (category, position) in enumerate(zip(random_object_category, random_positions), 1):
            row, col = position
            cell = self.grid[row][col]
            obj = Object(key, category, position, parent=cell)
            self.objects[key] = obj
            cell.object = obj

    def init_agents(self, n_agents, kplus, kminus, memory_buffer_size, error_rate):
        """Initialisation of the positions of the n_agents agents on the grid
        at n_agents random positions."""
        grid = [(row, col) for row in range(self.N)
                for col in range(self.M)]
        random_positions = random.sample(grid, n_agents)

        self.agents = {}

        for key, position in enumerate(random_positions, 1):
            # We instanciate an agent at the random position
            row, col = position
            cell = self.grid[row][col]
            agent = Agent(key, kplus, kminus, memory_buffer_size, error_rate)
            cell.agent = agent

            # We store this agent in an AgentData object that encapsulates the
            # agent and the position of the agent
            self.agents[key] = AgentData(agent, position)

    def valid_cell(self, row, col):
        return 0 <= row < self.N and 0 <= col < self.M

    def empty_cells(self, key, R=1):
        row, col = self.agents[key].position
        iterable = ((r, c) for r in range(row-R, row+R+1)
                    for c in range(col-R, col+R+1) if r != row or c != col)
        empty = []
        for row_, col_ in iterable:
            if self.valid_cell(row_, col_) and self.grid[row_][col_].agent is None:
                empty.append((row_, col_))
        return empty

    def move(self, key, destination):
        old_row, old_col = self.agents[key].position
        row, col = destination
        self.agents[key].position = destination
        agent = self.grid[old_row][old_col].agent
        self.grid[old_row][old_col].agent = None
        if self.grid[row][col].agent is not None:
            raise ValueError(
                f"There is already an agent in {(row, col)} where the agent {key} wants to go. Check the integrity")
        self.grid[row][col].agent = agent

    def get_agent_cell(self, key):
        row, col = self.agents[key].position
        return self.grid[row][col]


class Object:
    def __init__(self, key, category, position, parent):
        self.key = key
        self.category = category
        self.position = position
        self.parent = parent


class AgentData:
    def __init__(self, agent, position):
        self.agent = agent
        self.position = position


class Cell:
    def __init__(self, position, agent=None, obj=None):
        self.position = position
        self.agent = agent
        self.object = obj
