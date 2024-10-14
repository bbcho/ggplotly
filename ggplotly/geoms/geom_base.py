import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from itertools import product
from ..aes import aes
from ..stats.stat_base import Stat
from ..aes import aes
import copy


class Geom:
    """
    Base class for all geoms.
    """

    def __init__(self, data=None, mapping=None, **params):
        # check to see if data was passed first or if aes was passed first
        if isinstance(data, aes):
            self.mapping = data.mapping
            self.data = None
        else:
            self.data = data
            self.mapping = mapping.mapping if mapping else {}

        self.params = params
        self.stats = []
        self.layers = []

    # def __add__(self, other):
    #     if isinstance(other, Geom):
    #         self.layers.append(other)

    #     return self.copy()
    # else:
    # raise ValueError("Only Geom and Stat objects can be added to Geom objects.")

    def copy(self):
        new = copy.deepcopy(self)
        new.stats = [*self.stats.copy()]
        return new

    # def setup_data(self, data, plot_mapping):
    #     """
    #     Combine plot mapping with geom-specific mapping and set data.

    #     Parameters:
    #         data (DataFrame): The dataset to use.
    #         plot_mapping (dict): The global aesthetic mappings from the plot.
    #     """
    #     # Merge plot mapping and geom mapping, with geom mapping taking precedence
    #     combined_mapping = {**plot_mapping, **self.mapping}
    #     self.mapping = combined_mapping
    #     self.data = data.copy()

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw the geometry on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame): Optional data subset for faceting.
            row (int): Row position in subplot (for faceting).
            col (int): Column position in subplot (for faceting).
        """
        raise NotImplementedError("The draw method must be implemented by subclasses.")

    def _format_color_targets(self, color_targets, fill, color, size):
        # reverse dictionary color_targets
        color_targets = {v: k for k, v in color_targets.items()}

        for k, v in color_targets.items():
            # check to see if "fill" in is k
            if "fill" in v:
                color_targets[k] = fill
            elif "color" in v:
                color_targets[k] = color
            elif "size" in v:
                color_targets[k] = size

        # remove None values from color_targets
        color_targets = {k: v for k, v in color_targets.items() if v is not None}

        return color_targets

    def _transform_fig(
        self, plot, fig, data, payload, color_targets, row, col, **layout
    ):
        group_values = (
            data[self.mapping.get("group")] if "group" in self.mapping else None
        )

        (
            fill,
            fill_values,
            color,
            color_values,
            default_color,
            color_map,
            linetype,
            alpha,
            size,
        ) = self.handle_style(data, self.mapping, self.params)

        x = data[self.mapping["x"]] if "x" in self.mapping else None
        y = data[self.mapping["y"]] if "y" in self.mapping else None

        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    plot(
                        x=x[group_mask],
                        y=y[group_mask],
                        # mode="markers",
                        showlegend=self.params.get("showlegend", True),
                        marker=dict(
                            color=(
                                color_values[group_mask].iloc[0]
                                if color_values is not None
                                else default_color
                            ),
                            # size=size,
                        ),
                        opacity=alpha,
                        name=str(group),
                    ),
                    row=row,
                    col=col,
                )
        elif (color_values is not None) | (fill_values is not None):
            # COLOR and FILL GROUPS

            # check that both color and fill are not None
            if (color_values is not None) & (fill_values is not None):
                raise ValueError(
                    "If both color and fill are passed, only one can be a column name. The other must be a color value."
                )

            if color_values is not None:
                values = color_values
                value_col = color
            else:
                values = fill_values
                value_col = fill

            for key in values.keys():
                x = (
                    data.loc[data[value_col] == key, self.mapping["x"]]
                    if "x" in self.mapping
                    else None
                )
                y = (
                    data.loc[data[value_col] == key, self.mapping["y"]]
                    if "y" in self.mapping
                    else None
                )

                # bar geom only takes colors
                color_targets_final = self._format_color_targets(
                    color_targets, fill, values[key], size
                )
                # drop the key "name" from the payload
                if "name" in payload:
                    payload.pop("name")

                fig.add_trace(
                    plot(
                        x=x,
                        y=y,
                        # marker=dict(color=color_values[key], size=size),
                        opacity=alpha,
                        name=str(key),
                        showlegend=self.params.get("showlegend", True),
                        **payload,
                        **color_targets_final,
                    ),
                    row=row,
                    col=col,
                )
        else:
            if color_targets is not None:
                color_targets = self._format_color_targets(
                    color_targets, fill, color, size
                )

            fig.add_trace(
                plot(
                    x=x,
                    y=y,
                    opacity=alpha,
                    showlegend=self.params.get("showlegend", True),
                    **payload,
                    **color_targets,
                ),
                row=row,
                col=col,
            )

        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(**layout)

    def handle_style(self, data, mapping, params):
        """
        Shared color handler for geoms that maps continuous or categorical values to colors.

        Parameters:
            data (DataFrame): The data used for plotting.
            mapping (dict): Aesthetic mappings.
            params (dict): Additional parameters (e.g., default color).

        Returns:
            dict: A dictionary containing the mapped color values and color map.
        """
        color_map = (
            self.theme.color_map
            if hasattr(self.theme, "color_map") and self.theme.color_map
            else px.colors.qualitative.Plotly
        )

        # color keyword arg can either be a column name or a color value.
        # try to figure out which it is

        color = mapping.get("color") if "color" in mapping else None

        color_values = None
        try:
            # check to see if a column name was passed in the mapping
            color_values = data[mapping.get("color")]
        except:
            pass

        if color_values is not None:
            unique_colors = color_values.drop_duplicates()
            color_values = {
                val: color_map[i % len(color_map)]
                for i, val in enumerate(unique_colors)
            }

        # fill_values = data[mapping.get("fill")] if "fill" in mapping else None
        # fill = mapping.get("fill") if "fill" in mapping else None
        default_color = params.get("color", "#1f77b4")

        # color keyword arg can either be a column name or a color value.
        # try to figure out which it is

        fill = mapping.get("fill") if "fill" in mapping else None

        fill_values = None
        try:
            # check to see if a column name was passed in the mapping
            fill_values = data[mapping.get("fill")]
        except:
            pass

        if fill_values is not None:
            unique_fills = fill_values.drop_duplicates()
            fill_values = {
                val: color_map[i % len(color_map)] for i, val in enumerate(unique_fills)
            }

        return (
            fill,
            fill_values,
            color,
            color_values,
            default_color,
            color_map,
            self.params.get("linetype", "solid"),
            self.params.get("alpha", 1),
            self.params.get("size", 10),
        )
