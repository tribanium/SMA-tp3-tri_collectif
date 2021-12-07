#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Module with two helpers functions for visualization purposes.

@authors: Nathan Etourneau, Paul Flagel
"""

import altair as alt
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def update_altair_plot(env):
    """Returns an altair plot with the appropriate format."""
    obj_rows = []
    obj_cols = []
    obj_category = []
    for obj in env.objects.values():
        if obj.position:
            row, col = obj.position
            obj_rows.append(row)
            obj_cols.append(col)
            obj_category.append(obj.category)

    data = pd.DataFrame(
        {"row": obj_rows, "col": obj_cols, "category": obj_category})

    fig = alt.Chart(data).mark_circle().encode(
        x=alt.X('col', scale=alt.Scale(domain=[0, env.M])),
        y=alt.Y('row', scale=alt.Scale(domain=[0, env.N])),
        color=alt.Color(
            'category',
            legend=alt.Legend(orient='bottom'),
            scale=alt.Scale(range=['red', 'green', 'blue'])
        )
    ).configure_axis(
        grid=False
    ).properties(
        width=600, height=600
    )
    return fig


def update_matplotlib_plot(env, ax):
    """Returns a matplotlib figure with the appropriate format."""
    ax.clear()

    obj_rows = []
    obj_cols = []
    obj_category = []
    for obj in env.objects.values():
        if obj.position is None:
            continue
        row, col = obj.position

        obj_rows.append(row)
        obj_cols.append(col)
        obj_category.append(obj.category)

    data = pd.DataFrame(
        {"rows": obj_rows, "cols": obj_cols, "category": obj_category})

    ax = sns.scatterplot(x='cols', y='rows', data=data,
                         hue='category', style='category', ec=None)
    ax.set_xlim(-1, env.M)
    ax.set_ylim(-1, env.N)
    plt.show()
