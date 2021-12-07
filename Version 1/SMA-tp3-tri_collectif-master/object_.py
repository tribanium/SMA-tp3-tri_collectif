#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with an Object class used to modelize the objects in the grid. An object 
is described by its category, its position, and its parent : a Cell object, or
an Agent object, depending on what kind of thing is holding the object.

@authors: Nathan Etourneau, Paul Flagel
"""


class Object:
    """An Object class used to modelize the objects in the grid. It has 4 
    attributes : key : the key of the object, category : the category of the 
    object, position : it the object is in the grid, its a tuple with its 
    position, and if the object is carried by an agent, it is None."""

    def __init__(self, key, category, position, parent):
        """Instanciates an Object object

        Args:
            - key (str): The key of the object for further reference to it.

            - category (str): A character encoding the category of the object.

            - position (tuple[int, int] or None): If the object is in the grid, 
            a tuple in the form (row, col). If the object is carried by an 
            agent, it is None.

            - parent (Cell or Agent): The object that holds the object. It can be
            a Cell instance or an Agent instance.
        """
        self.key = key
        self.category = category
        self.position = position
        self.parent = parent
