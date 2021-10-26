#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main module coding the loop

@authors: Nathan Etourneau, Paul Flagel
"""

import random

import streamlit as st
import plotly.express as px

from agent import Agent
from environment import Environment

# Sidebar

st.sidebar.header("General settings")

N = st.sidebar.number_input(
    label="Number of rows ?", min_value=1, max_value=99999, value=50)
M = st.sidebar.number_input(
    label="Number of columns ?", min_value=1, max_value=99999, value=50)
NA = st.sidebar.number_input(
    label="Number of objects of class A ?", min_value=1, max_value=99999, value=200)
NB = st.sidebar.number_input(
    label="Number of objects of class B ?", min_value=1, max_value=99999, value=200)
N_AGENTS = st.sidebar.number_input(
    label="Number of agents ?", min_value=1, max_value=99999, value=20)
KPLUS = st.sidebar.slider(label="Value for K+ ?",
                          min_value=0., max_value=1., value=0.1)
KMINUS = st.sidebar.slider(label="Value for K- ?",
                           min_value=0., max_value=1., value=0.3)
MEMORY_BUFFER_SIZE = st.sidebar.number_input(
    label="Size of memory buffer ?", min_value=1, max_value=99999, value=15)
N_ROUNDS = st.sidebar.number_input(
    label="Number of rounds ?", min_value=1, max_value=1000000000, value=500000)
start = st.sidebar.button("Run")

# Layout

st.title("Practical work 3 : Multi-agents implementation")
st.markdown(
    """Authors : @paulflagel, @nathanetourneau.

A school project focused on the implementation of this research paper : Deneubourg, Jean-Louis, Simon Goss, Nigel R. Franks, Ana B. Sendova-Franks, Claire Detrain and Louis Chretien. “The dynamics of collective sorting robot-like ants and ant-like robots.” (1991).

Master 2 IA - Université Lyon 1 - 2021-2022"""
)


status = st.empty()
round_progress_bar = st.progress(0)
st.header('Graph of the objects')
plot_placeholder = st.empty()


def update_plot(env):
    obj_rows = []
    obj_cols = []
    obj_category = []
    for obj in env.objects.values():
        row, col = obj.position

        obj_rows.append(row)
        obj_cols.append(col)
        obj_category.append(obj.category)

    data = {"rows": obj_rows, "cols": obj_cols, "category": obj_category}

    fig = px.scatter(data, x="rows", y="cols",
                     color="category", width=800, height=800)
    fig.update_xaxes(range=[0-1, M+1])
    fig.update_yaxes(range=[0-1, N+1])

    return fig


def main():
    env = Environment(N, M, NA, NB, N_AGENTS, KPLUS,
                      KMINUS, MEMORY_BUFFER_SIZE)

    # Loop
    agent_keys = list(env.agents.keys())

    for round in range(1, N_ROUNDS+1):
        status.text(f'Round n°{round}/{N_ROUNDS}')
        round_progress_bar.progress(round/N_ROUNDS)

        # Shuffle the agents to mimic the fact that the movement is erratic
        random.shuffle(agent_keys)

        for key in agent_keys:
            agent = env.agents[key].agent
            agent.perception(env)
            agent.action(env)
        if round % 300 == 0 or round == 1:
            fig = update_plot(env)
            plot_placeholder.plotly_chart(fig, use_container_width=True)


if start:
    main()
