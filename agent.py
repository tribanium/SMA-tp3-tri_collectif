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
        self.object = None
        self.error_rate = error_rate

    def perception(self, environment):
        return environment.empty_cells(self.key)

    def action(self, environment, empty_cells):
        if empty_cells:
            destination = random.choice(empty_cells)
            environment.move(self.key, destination)

        cell = environment.get_agent_cell(self.key)
        to_push = cell.object.category if cell.object is not None else '0'

        if self.object:
            if cell.object is None and self.will_drop(self.object.category):
                cell.object = self.object
                self.object = None
                cell.object.parent = cell
                cell.object.position = cell.position

        elif cell.object is not None and self.will_pick(cell.object.category):

            self.object = cell.object
            cell.object = None

            self.object.position = None
            self.object.parent = self

        self.update_memory(to_push)

    def update_memory(self, category):
        if category is None:
            category = '0'

        assert type(category) == str

        if self.memory:
            if len(self.memory) >= self.memory_buffer_size:
                self.memory = category + \
                    self.memory[:self.memory_buffer_size-1]
            else:
                self.memory = category + self.memory
        else:
            self.memory = category + self.memory

    def get_frequency(self, category):
        if self.memory:
            count = self.memory.count(category)
            count_empty = self.memory.count('0')
            count_other = len(self.memory) - count - count_empty
            return (count + self.error_rate * count_other) / len(self.memory)
        return 0

    def will_pick(self, category):
        f = self.get_frequency(category)
        p = (self.kplus / (self.kplus + f)) ** 2
        return random.random() <= p

    def will_drop(self, category):
        f = self.get_frequency(category)
        p = (f / (self.kminus + f)) ** 2
        return random.random() <= p
