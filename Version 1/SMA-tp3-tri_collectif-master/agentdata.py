#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with an AgentData classthat encapsulates an agent and its position. Its 
main purpose is to store the position of the agents without the position being 
an attribute of the agent.

@authors: Nathan Etourneau, Paul Flagel
"""


class AgentData:
    """An AgentData class that encapsulates an agent and its position. Its 
main purpose is to store the position of the agents without the position being 
an attribute of the agent. It has two attributes : agent : the agent whose data
is being stored, and position : the position of the same agent."""

    def __init__(self, agent, position):
        """Instanciates an AgentData object

        Args:
            - agent (Agent): The agent that one wants to store data on.

            - position (tuple[int, int]): The position of the same agent.
        """
        self.agent = agent
        self.position = position
