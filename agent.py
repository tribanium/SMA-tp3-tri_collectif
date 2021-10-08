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
        pass

    def action(self):
        if not self.is_binded_with:


    def move(self, environment):
        position = environment.agents[self.key]
        environment.move(position)
        row, col = position
        self.memory = environment.object_grid[row][col] + self.memory[0:-1]

        directions = [
                (1,0), (1,1), (0,1), (-1,1),
                (-1, 0), (-1, -1), (0, -1), (1, -1)
            ]
        random.shuffle(directions)

        move = None


        try:
            # This loop will look for a valid move
            while not move:
                move = directions.pop()  # We choose randomly a direction

                if self.is_valid_move(position, move):
                    break  # A valid direction has been found
                else:
                    move = None  # The move wasn't valid

        # No direction is valid so the agent doesn't move
        except IndexError:
            move = (0, 0)


