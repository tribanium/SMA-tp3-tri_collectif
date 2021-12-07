#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with a Cell class that encapsulates the logic that happens in a cell of 
the grid. A cell can hold an object, an agent or both. The cell object also 
stores its position on the grid.

@authors: Nathan Etourneau, Paul Flagel
"""


class Cell:
    """A Cell class that encapsulates the logic happening in a cell of a grid.
A cell can contain an object, an agent or both of them. Then, the grid will 
be a collection of cells. 

The cell object has 3 attributes : 
    - position : a tuple in the form (row, col) coding the position of the cell

    - agent : if there is an agent on the cell, contains that agent, otherwise it contains None. 

    - object : if there is an object on the cell, contains that object, otherwise it contains None.
    """

    def __init__(self, position, agent=None, obj=None):
        """Instanciates a Cell object

        Args:
            - position (tuple[int, int]): A tuple in the form (row, col) with 
            the position of the agent.

            - agent (Agent, optional): The potential agent on the cell. 
            Defaults to None.

            - obj (Object, optional): The potential object on the cell. 
            Defaults to None.
        """
        self.position = position
        self.agent = agent
        self.object = obj
