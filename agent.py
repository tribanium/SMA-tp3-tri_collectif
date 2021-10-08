#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Module with a class Agent used to modelize an agent in a multi-agent system.

@authors: Nathan Etourneau, Paul Flagel
"""


class Agent:

    def __init__(self, key, kplus, kminus):
        self.memory = ''
        self.key = key
        self.kplus = kplus
        self.kminus = kminus
        self.is_binded_with = None

    def perception(self, environment):
        row, col = environment.agents[self.key]
        self.memory = environment.object_grid[row][col] + self.memory[0:-1]

    def action(self):
        if not self.is_binded_with:

    def move(self, environment):
        position = environment.agents[self.key]
        environment.move(position)
        row, col = position
        self.memory = environment.object_grid[row][col] + self.memory[0:-1]

