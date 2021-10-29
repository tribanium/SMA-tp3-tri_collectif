#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with a class Environment used to modelize the environment in a 
multi-agent system.

@authors: Nathan Etourneau, Paul Flagel
"""

import random

from agent import Agent
from agentdata import AgentData
from cell import Cell
from object_ import Object


class Environment:
    """An Environment class that wraps all the data needed for the multi-agent 
    experiment. The agents only have to make requests to the Environment
    object. Is instancied only once.
    """

    def __init__(self, N, M, na, nb, n_agents, kplus, kminus, memory_buffer_size=15, error_rate=0):
        """Instanciates the Environment object. The environment contains a 
        dict of Agent objects, a dict of Object objects, a grid containing 
        Cell objects.

        Args:
            - N (int): Number of rows in the grid.

            - M (int): Number of columns in the grid.

            - na (int): Number of objects of class A.

            - nb (int): Number of objects of class B.

            - n_agents (int): Number of agents.

            - kplus (float): Value of k+ as described in the paper.

            - kminus (float): Value of k- as described in the paper.

            - memory_buffer_size (int, optional): Size of the memory as 
            described in the paper. Defaults to 15.

            - error_rate (float, optional): Error rate in the object class 
            recognition, as described in the paper. Defaults to 0.
        """

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
        """Instanciates na objects of category A and nb objects of category B 
        at na + nb random positions on the grid

        Args:
            - na (int): Number of objects of class A.

            - nb (int): Number of objects of class B.
        """

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
        """Instanciates n_agents agents on the grid at n_agents random 
        positions.

        Args:
            - n_agents (int): Number of agents.

            - kplus (float): Value of k+ as described in the paper.

            - kminus (float): Value of k- as described in the paper.

            - memory_buffer_size (int): Size of the memory as 
            described in the paper.

            - error_rate (float): Error rate in the object class 
            recognition, as described in the paper.
        """
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
        """Checks if the cell located at (row, col) is in bounds or out of 
        bounds.

        Args:
            - row (int): The row one wants to check the validity.

            - col (int): The column one wants to check the validity.

        Returns:
            bool : True if the cell is valid, False otherwise.
        """
        return 0 <= row < self.N and 0 <= col < self.M

    def empty_cells(self, key, R=1):
        """Given an agent key, returns the empty cells around it, in the given 
        radius.

        Args:
            - key (int): The key of the agent one wants the empty cells around.

            - R (int, optional): The radius up to where to look for empty 
            cells. Defaults to 1.

        Returns:
            List[tuple[int, int]]: The list of the empty cells around the 
            agent. The format is (drow, dcol) where drow is the vertical 
            movement and dcol is the horizontal movement.
        """
        row, col = self.agents[key].position
        iterable = ((drow, dcol) for drow in range(-R, R+1)
                    for dcol in range(-R, R+1) if drow != 0 or dcol != 0)
        empty = []
        for drow, dcol in iterable:
            new_row = row + drow
            new_col = col + dcol

            if self.valid_cell(new_row, new_col) and self.grid[new_row][new_col].agent is None:
                empty.append((drow, dcol))
        return empty

    def move(self, key, direction):
        """Given an agent key, and a destination with the format (row, col), 
        moves the agent to the specified destination, ensuring the integrity of 
        the grid.

        Args:
            - key (int): The key of the agent one wants to move.

            - direction (tuple[int, int]): The direction where one wants 
            the agent to go, with the format (drow, dcol). (The d stands for 
            delta, which mean the direction is relative to the actual position
            of the agent).

        Raises:
            - ValueError: There is an agent at the given destination. The 
            integrity isn't respected.
        """
        old_row, old_col = self.agents[key].position
        drow, dcol = direction

        new_row = old_row + drow
        new_col = old_col + dcol
        destination = (new_row, new_col)

        agent = self.grid[old_row][old_col].agent

        if self.grid[new_row][new_col].agent is not None:
            raise ValueError(
                f"There is already an agent in {(new_row, new_col)} where the agent {key} wants to go. Check the integrity")

        self.agents[key].position = destination
        self.grid[new_row][new_col].agent = agent
        self.grid[old_row][old_col].agent = None

    def get_agent_cell(self, key):
        """Given an agent key, returns the Cell object where the agent is 
        located.

        Args:
            - key (int): The key of the agent one wants to obtain the cell 
            below.

        Returns:
            - Cell: The cell where the agent with the given key is located.
        """
        row, col = self.agents[key].position
        return self.grid[row][col]
