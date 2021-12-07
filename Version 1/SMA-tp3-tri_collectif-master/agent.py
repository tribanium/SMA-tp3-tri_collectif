#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with a class Agent used to modelize an agent in a multi-agent system.

@authors: Nathan Etourneau, Paul Flagel
"""

import random


class Agent:
    """An Agent class that encapsulates all the logic than happens on the agent 
    side of a multi-agent system. Its contains a lot of helpers methods, the 
    main methods being perception and action, all the other are used for this 
    purpose.
    """

    def __init__(self, key, kplus, kminus, memory_buffer_size=15, error_rate=0):
        """Instanciates an Agent object

        Args:
            - key (int): The key of the agent, for further identification

            - kplus ([type]):  Value of k+ as described in the paper.

            - kminus ([type]):  Value of k- as described in the paper.

            - memory_buffer_size (int, optional): Size of the memory as 
            described in the paper. Defaults to 15.

            - error_rate (float, optional): Error rate in the object class 
            recognition, as described in the paper. Defaults to 0.
        """
        self.memory = ""
        self.key = key
        self.kplus = kplus
        self.kminus = kminus
        self.memory_buffer_size = memory_buffer_size
        self.object = None
        self.error_rate = error_rate

    def perception(self, environment):
        """Request to the environment the empty (without an agent) cells positions
        around. Returns the list of empty cells around.

        Args:
            - environment (Environment): The Environment object.

        Returns:
            - List[tuple[int, int]]: The list of the directions leading to an 
            empty cell
        """
        return environment.empty_cells(self.key)

    def action(self, environment, empty_cells):
        """Given the empty cells around, act consequently.

        - The first step is to move randomly to an empty cell.
        - Then, if an object is bound, the cell is empty and the random event of 
        dropping an object occurs, the object is dropped. 
        - If no object is bound, if the current cell contains an object and 
        the random event of picking an object occurs, the object is picked.

        The memory is then updated with what was on the cell before picking or 
        dropping anything (after the random move of the first cell).


        Args:
            - environment (Environment)): The Environment object.

            - empty_cells (List[tuple[int, int]]): The list of the empty cells 
            around this current Agent instance.
        """

        # In the article, the first step is to move randomly

        # If there are available cells around, we choose one and we go there
        if empty_cells:
            destination = random.choice(empty_cells)
            environment.move(self.key, destination)

        # We keep in mind the current cell category
        cell = environment.get_agent_cell(self.key)
        to_push = cell.object.category if cell.object is not None else '0'

        # If the error rate is enabled, there can be an error of classification
        if self.error_rate > 0:
            if random.random() <= self.error_rate:
                if to_push == 'A':
                    to_push = 'B'
                elif to_push == 'B':
                    to_push = 'A'

        # If an object is bound :
        if self.object:
            # If the cell is empty and the random event of dropping occurs :
            if cell.object is None and self.will_drop(self.object.category):

                # The object is freed from the agent, and bound to the cell
                cell.object = self.object

                # No object is left to the agent
                self.object = None

                # The parent of the object becomes the cell, no longer the agent
                cell.object.parent = cell

                # We update object position (when bound, it is None)
                cell.object.position = cell.position

        # If no object is bound, there is an object on the cell and the random event of picking it occurs :
        elif cell.object is not None and self.will_pick(cell.object.category):

            # The object is freed from the cell, and bound to the agent
            self.object = cell.object

            # There is no object left in the cell
            cell.object = None

            # Until it is dropped, the position is not defined
            self.object.position = None

            # The parent of the object becomes the agent, it's no longer the cell
            self.object.parent = self

        # We update the memory with what was in the cell before we picked/dropped anything
        self.update_memory(to_push)

    def update_memory(self, category):
        """Updates the memory with the new category observed (it can be '0' 
        if there is no object on a cell)

        Args:
            category (str or None): The category of the last object seen.
        """
        if category is None:
            category = '0'

        if len(self.memory) >= self.memory_buffer_size:
            self.memory = category + self.memory[:self.memory_buffer_size-1]
        else:
            self.memory = category + self.memory

    def get_frequency(self, category):
        """Computes the frequency of appearance of the given category in the 
        memory, and takes into account the error rate.

        Args:
            - category (str): The object category one wants to compute the 
            frequency.

        Returns:
            float: The frequency in the memory of the given object category.
        """
        if self.memory:
            count = self.memory.count(category)
            count_empty = self.memory.count('0')
            count_other = len(self.memory) - count - count_empty
            return (count + self.error_rate * count_other) / len(self.memory)
        return 0

    def will_pick(self, category):
        """Returns a boolean whether to pick an object of the given category, 
        given the memory state.

        Args:
            - category (str): The object category one wants to know whether to 
            pick it or not

        Returns:
            bool: True if the Agent object picks the object, False otherwise.
        """
        f = self.get_frequency(category)
        p = (self.kplus / (self.kplus + f)) ** 2
        return random.random() <= p

    def will_drop(self, category):
        """Returns a boolean whether to drop an object of the given category, 
        given the memory state.

        Args:
            - category (str): The object category one wants to know whether to 
            drop it or not

        Returns:
            bool: True if the Agent object drops the object, False otherwise.
        """
        f = self.get_frequency(category)
        p = (f / (self.kminus + f)) ** 2
        return random.random() <= p
