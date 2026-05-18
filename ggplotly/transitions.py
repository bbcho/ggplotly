"""Small gganimate-style transition helpers."""

from __future__ import annotations

import copy

import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp


class Transition:
    """Build Plotly frames from a ggplotly data field."""

    def __init__(self, field, mode="time"):
        self.field = field
        self.mode = mode

    def copy(self):
        return copy.deepcopy(self)

    def _mask(self, data, value):
        if self.field not in data.columns:
            return pd.Series([True] * len(data), index=data.index)
        if self.mode == "reveal":
            return data[self.field] <= value
        return data[self.field] == value

    def apply(self, plot, fig):
        data = plot.data
        if data is None or self.field not in data.columns:
            return
        values = list(pd.Series(data[self.field]).dropna().sort_values().unique())
        if not values:
            return

        frames = []
        for value in values:
            frame_fig = sp.make_subplots(rows=1, cols=1)
            for geom in plot.layers:
                draw_geom = geom.copy()
                geom_data = draw_geom.data if draw_geom.data is not None else data
                if geom_data is not None and self.field in geom_data.columns:
                    frame_data = geom_data[self._mask(geom_data, value)].copy()
                else:
                    frame_data = geom_data
                draw_geom.draw(frame_fig, data=frame_data, row=1, col=1)
            frames.append(go.Frame(data=list(frame_fig.data), name=str(value)))

        fig.frames = frames
        fig.update_layout(
            updatemenus=[{
                "type": "buttons",
                "showactive": False,
                "buttons": [
                    {
                        "label": "Play",
                        "method": "animate",
                        "args": [None, {"frame": {"duration": 450, "redraw": True}, "fromcurrent": True}],
                    },
                    {
                        "label": "Pause",
                        "method": "animate",
                        "args": [[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}],
                    },
                ],
            }],
            sliders=[{
                "steps": [
                    {
                        "label": str(value),
                        "method": "animate",
                        "args": [[str(value)], {"frame": {"duration": 0, "redraw": True}, "mode": "immediate"}],
                    }
                    for value in values
                ],
            }],
        )


def transition_time(time):
    return Transition(time, mode="time")


def transition_states(states):
    return Transition(states, mode="states")


def transition_reveal(along):
    return Transition(along, mode="reveal")
