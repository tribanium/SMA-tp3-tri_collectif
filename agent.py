#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random

"""
Module with a class Agent used to modelize an agent in a multi-agent system.

@authors: Nathan Etourneau, Paul Flagel
"""


class Agent:
    def __init__(self, key, kplus, kminus):
        self.memory = ""
        self.key = key
        self.kplus = kplus
        self.kminus = kminus
        self.is_binded_with = None

    def perception(self, environment):
        pass

    def action(self):
        if not self.is_binded_with:
            pass

    def move(self, environment):
        self.memory = environment.object_grid[row][col] + self.memory[0:-1]
        directions = [
            (1, 0),
            (1, 1),
            (0, 1),
            (-1, 1),
            (-1, 0),
            (-1, -1),
            (0, -1),
            (1, -1),
        ]
        random.shuffle(directions)

        displacement = None

        try:
            # This loop will look for a valid displacement
            while not displacement:
                displacement = directions.pop()  # We choose randomly a direction

                if environment.is_valid_move(self.key, displacement):
                    break  # A valid direction has been found
                else:
                    displacement = None  # The displacement wasn't valid

        # No direction is valid so the agent doesn't move
        except IndexError:
            displacement = (0, 0)




