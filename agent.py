#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import numpy as np

"""
Module with a class Agent used to modelize an agent in a multi-agent system.

@authors: Nathan Etourneau, Paul Flagel
"""


class Agent:
    def __init__(self, key, kplus, kminus, memory_buffer_size=15, error_rate=0.):
        self.memory = ""
        self.key = key
        self.kplus = kplus
        self.kminus = kminus
        self.memory_buffer_size = memory_buffer_size
        self.bound_object = None
        self.error_rate = error_rate

    def perception(self, environment):
        return environment.perception(self.key)

    def action(self, environment):
        _, _, object_free_cells_around, agent_free_cells_around = self.perception(
            environment)

        if self.is_bound_with:
            available_directions = [
                dir for dir in agent_free_cells_around if dir in object_free_cells_around]

            if available_directions:
                direction = random.choice(available_directions)

            else:
                direction = (0, 0)

        else:
            if agent_free_cells_around:
                direction = random.choice(agent_free_cells_around)

            else:
                direction = (0, 0)

        environment.move_agent(self.key, direction)
        if self.is_bound_with:
            environment.move_object(self.bound_object.key, direction)

        cell = environment.get_agent_cell(self.key)

        if self.bound_object:
            category = self.bound_object.category

            if not cell.object and self.will_drop(category):
                self.bound_object.is_bound = False
                self.bound_object = None

        elif cell.object:
            if self.will_pick(cell.object.category):
                self.bound_object = cell.object
                cell.is_bound_with = self

        self.update_memory(cell.object)

    def update_memory(self, category):
        if category is None:
            category = '0'
        if self.memory:
            self.memory = category + self.memory[:-1]

    def get_frequency(self, category):
        if self.memory:
            count = self.memory.count(category)
            return count / len(self.memory)
        return 0

    def will_pick(self, category):
        f = self.get_frequency(category)
        p = (self.kplus / (self.kplus + f)) ** 2
        return random.random() <= p

    def will_drop(self, category):
        f = self.get_frequency(category)
        p = (f / (self.kminus + f)) ** 2
        return random.random() <= p
