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
    def __init__(self, N, M, na, nb, n_agents, kplus, kminus, memory_buffer_size=15):
        self.N = N
        self.M = M
        self.na = na
        self.nb = nb

        self.n_agents = n_agents
        self.kplus = kplus
        self.kminus = kminus
        self.memory_buffer_size = memory_buffer_size

        self.grid = [[Cell() for _ in range(M)] for _ in range(N)]
        self.init_grid()

    def init_grid(self):
        self.init_objects()
        self.init_agents()

        for obj in self.objects:
            row, col = obj.position
            self.grid[row][col].obj = obj

        for agent_data in self.agents:
            row, col = agent_data.position
            self.grid[row][col].agent = agent_data.agent

    def init_objects(self):
        """Instanciation of na objects of category A and nb objects of category B at
        na + nb random positions on the grid"""

        grid = [(row, col) for row in range(self.N)
                for col in range(self.M)]
        random_positions = random.sample(grid, self.na + self.nb)
        random_object_category = random.sample(
            self.na * "A" + self.nb * "B", self.na + self.nb)

        self.objects = {}

        for key, (category, position) in enumerate(zip(random_object_category, random_positions), 1):
            self.objects[key] = Object(key, category, position)

    def init_agents(self):
        """Initialisation of the positions of the n_agents agents on the grid
        at n_agents random positions."""
        grid = [(row, col) for row in range(self.N)
                for col in range(self.M)]
        random_positions = random.sample(grid, self.n_agents)

        self.agents = {}
        self.agent_positions = [
            [None for _ in range(self.M)] for _ in range(self.N)
        ]

        for key, position in enumerate(random_positions, 1):
            # We instanciate an agent at the random position
            row, col = position
            agent = Agent(key, self.kplus, self.kminus,
                          self.memory_buffer_size)

            # We store this agent in an AgentData object that encapsulates the
            # agent and the position of the agent
            self.agents[key] = AgentData(
                agent=agent,
                position=position)

    def perception(self, key, radius=1):
        row, col = self.agents[key].position

        objects_around = []
        agents_around = []
        free_cells_around = []

        for drow in range(-radius, radius+1):
            for dcol in range(-radius, radius+1):
                if drow == 0 and dcol == 0:
                    continue

                if 0 <= row+drow <= self.N and 0 <= col+dcol <= self.M:
                    cell = self.grid[row][col]

                    if cell.agent:
                        direction = (drow, dcol)
                        agents_around.append(direction)

                    else:
                        direction = (drow, dcol)
                        free_cells_around.append(direction)

                    if cell.object:
                        object_data = {"direction": (
                            drow, dcol), "category": cell.object.category}
                        objects_around.append(object_data)

            cell = environment.grid[row][col]

        return cell, objects_around, agents_around, object_free_cells_around, agent_free_cells_around


class Object:
    def __init__(self, key, category, position):
        self.key = key
        self.category = category
        self.position = position
        self.is_bound_with = None


class AgentData:
    def __init__(self, agent, position):
        self.agent = agent
        self.position = position
