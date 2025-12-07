"""Polar coordinate system for circular plots."""

import numpy as np
import plotly.graph_objects as go
from .coord_base import Coord


class coord_polar(Coord):
    """
    Polar coordinate system for circular/radial plots.

    Transforms cartesian coordinates into polar coordinates where
    one variable maps to angle and the other to radius. Useful for pie charts,
    radar charts, wind roses, and other circular visualizations.

    Parameters:
        theta (str): Variable that maps to angle. Either 'x' (default) or 'y'.
            If 'x', x values map to angle and y to radius.
            If 'y', y values map to angle and x to radius.
        start (float): Offset of starting point from 12 o'clock in radians.
            Default is 0 (start at 12 o'clock).
        direction (int): 1 for clockwise (default), -1 for counterclockwise.
        clip (str): Should drawing be clipped to the extent of the plot panel?
            Options: 'on' (default), 'off'.

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + geom_bar() + coord_polar()
        >>> ggplot(df, aes(x='category', y='value')) + geom_bar() + coord_polar(theta='y')
        >>> ggplot(df, aes(x='wind_dir', y='speed')) + geom_bar() + coord_polar(start=np.pi/2)
        >>> ggplot(df, aes(x='category', y='value')) + geom_bar() + coord_polar(direction=-1)
    """

    def __init__(self, theta='x', start=0, direction=1, clip='on'):
        """
        Initialize the polar coordinate system.

        Parameters:
            theta (str): Variable that maps to angle ('x' or 'y'). Default is 'x'.
            start (float): Starting angle offset in radians. Default is 0.
            direction (int): 1 for clockwise, -1 for counterclockwise. Default is 1.
            clip (str): Clipping mode ('on' or 'off'). Default is 'on'.
        """
        if theta not in ('x', 'y'):
            raise ValueError("theta must be 'x' or 'y'")
        if direction not in (1, -1):
            raise ValueError("direction must be 1 (clockwise) or -1 (counterclockwise)")

        self.theta = theta
        self.start = start
        self.direction = direction
        self.clip = clip

    def apply(self, fig):
        """
        Apply polar coordinate transformation to the figure.

        Converts cartesian traces to polar equivalents:
        - Bar traces -> Pie chart (when theta='x') or Barpolar (when theta='y')
        - Scatter traces -> Scatterpolar

        Parameters:
            fig (Figure): Plotly figure object.
        """
        # Convert start from radians to degrees for Plotly
        # Plotly's rotation is counterclockwise from 3 o'clock position
        # ggplot2's start is from 12 o'clock position
        # Convert: ggplot2 0 rad from 12 o'clock = Plotly 90 degrees from 3 o'clock
        start_degrees = 90 - np.degrees(self.start)

        # Direction: Plotly uses 'counterclockwise' or 'clockwise'
        # ggplot2: 1 = clockwise, -1 = counterclockwise
        angular_direction = 'clockwise' if self.direction == 1 else 'counterclockwise'

        # Check if we have Bar traces - convert to Pie or Barpolar
        bar_traces = [t for t in fig.data if t.type == 'bar']
        scatter_traces = [t for t in fig.data if t.type == 'scatter']
        other_traces = [t for t in fig.data if t.type not in ('bar', 'scatter')]

        new_traces = []

        # Convert Bar traces
        if bar_traces:
            # Combine all bar traces into a single pie chart
            # This matches the common ggplot2 pattern: geom_bar() + coord_polar()
            all_labels = []
            all_values = []
            all_colors = []

            for trace in bar_traces:
                if self.theta == 'x':
                    # theta='x': x maps to angle (labels), y maps to size (values)
                    labels = trace.x if trace.x is not None else []
                    values = trace.y if trace.y is not None else []
                else:
                    # theta='y': y maps to angle (labels), x maps to size (values)
                    labels = trace.y if trace.y is not None else []
                    values = trace.x if trace.x is not None else []

                if len(labels) > 0 and len(values) > 0:
                    all_labels.extend(labels if hasattr(labels, '__iter__') and not isinstance(labels, str) else [labels])
                    all_values.extend(values if hasattr(values, '__iter__') else [values])
                    # Get color from marker
                    if hasattr(trace, 'marker') and trace.marker is not None:
                        color = trace.marker.color
                        if isinstance(color, str):
                            all_colors.extend([color] * (len(labels) if hasattr(labels, '__iter__') and not isinstance(labels, str) else 1))
                        elif hasattr(color, '__iter__'):
                            all_colors.extend(color)

            # Create pie trace
            pie_kwargs = dict(
                labels=all_labels,
                values=all_values,
                rotation=start_degrees,
                direction=angular_direction,
                hole=0,  # No hole by default
            )

            if all_colors:
                pie_kwargs['marker'] = dict(colors=all_colors)

            new_traces.append(go.Pie(**pie_kwargs))

        # Convert Scatter traces to Scatterpolar
        for trace in scatter_traces:
            if self.theta == 'x':
                theta_values = trace.x
                r_values = trace.y
            else:
                theta_values = trace.y
                r_values = trace.x

            scatterpolar_kwargs = dict(
                r=r_values,
                theta=theta_values,
                mode=trace.mode if trace.mode else 'lines',
                name=trace.name,
            )

            if hasattr(trace, 'marker') and trace.marker is not None:
                scatterpolar_kwargs['marker'] = dict(
                    color=trace.marker.color,
                    size=trace.marker.size,
                )

            if hasattr(trace, 'line') and trace.line is not None:
                scatterpolar_kwargs['line'] = dict(color=trace.line.color)

            new_traces.append(go.Scatterpolar(**scatterpolar_kwargs))

        # Keep other traces as-is (they might already be polar)
        new_traces.extend(other_traces)

        # Replace all traces
        fig.data = []
        for trace in new_traces:
            fig.add_trace(trace)

        # Set up polar layout (for non-pie traces) or hide legend for pie
        has_pie = any(t.type == 'pie' for t in fig.data)
        if has_pie:
            # Hide legend for pie charts (categories shown in pie itself)
            fig.update_layout(showlegend=False)
        else:
            # Set up polar layout for scatterpolar/barpolar traces
            polar_config = dict(
                radialaxis=dict(visible=True),
                angularaxis=dict(
                    visible=True,
                    rotation=start_degrees,
                    direction=angular_direction,
                ),
            )
            fig.update_layout(polar=polar_config)
