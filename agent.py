#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import numpy as np

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
        """Looks at the current case, updates memory and returns cell data"""
        obj_class, _ = environment.get_case_data(self.key)

        if self.memory:
            if len(self.memory) == 15:
                self.memory = obj_class + self.memory[0:-1]
            else:
                self.memory = obj_class + self.memory
        else:
            self.memory = obj_class

    def action(self, environment):
        """Either pick an object, or if an object was already picked, drops it,
        or move randomly"""

        # If an object is binded, do we drop it ?
        if self.is_binded_with:
            if self.probability_dropping_object():
                self.is_binded_with = None
                return

        # If an object is on the case with no object binded, do we pick it ?
        elif self.memory[0] != '0':
            if self.probability_picking_object():
                _, obj_key = environment.get_case_data(self.key)
                self.is_binded_with = obj_key
                return

        # If we are here, no object has been picked or dropped, so the agent
        # moves randomly

        # We look for a valid displacement
        displacement = self.find_displacement(environment)

        # We move the agent, and if needed the object accordingly
        environment.move_agent(self.key, displacement)
        if self.is_binded_with:
            environment.move_object(self.is_binded_with, displacement)

    def probability_picking_object(self):
        """Computes the probability p of picking an object, using the memory as
        an approximation of the environment and draws True or False according
        to this Bernoulli distribution"""
        obj_category = self.memory[0]  # Last cell data
        f = self.memory.count(obj_category)/len(self.memory)
        p = (self.kplus/(self.kplus + f))**2
        result = np.random.binomial(1, p)
        return bool(result)

    def probability_dropping_object(self):
        """Computes the probability p of dropping an object, using the memory
        as an approximation of the environment and draws True or False
        according to this Bernoulli distribution"""
        obj_category = self.memory[0]  # Last cell data
        f = self.memory.count(obj_category)/len(self.memory)
        p = (f/(self.kminus + f))**2
        result = np.random.binomial(1, p)
        return bool(result)

    def find_displacement(self, environment):
        """Returns a displacement suitable for the agent, and if the agent is
        bound to an object, a displacement that is also suitable for the object
        """
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
        # TODO : change probabilities to reflect that cases
        # with an object are more attractive and that directions aren't equal
        # in probabilities

        displacement = None

        # This loop will look for a valid displacement
        while directions:
            # We choose one element in the list of possible directions
            displacement = directions.pop()

            # We check if the displacement is valid

            # Valid for the agent
            valid_agent_move = environment.is_valid_agent_move(
                self.key, displacement)

            # And valid for the object
            if self.is_binded_with:
                valid_object_move = environment.is_valid_object_move(
                    self.is_binded_with, displacement)

            # No object case, obviously valid
            else:
                valid_object_move = True

            # If the displacement is suitable for the object and
            # the agent, we return it
            if valid_agent_move and valid_object_move:
                return displacement

        # No direction is valid so the agent doesn't move at this stage
        displacement = (0, 0)
        return displacement
