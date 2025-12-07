"""Polar coordinate system for circular plots."""

import numpy as np
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

        polar_config = dict(
            radialaxis=dict(visible=True),
            angularaxis=dict(
                visible=True,
                rotation=start_degrees,
                direction=angular_direction,
            ),
        )

        fig.update_layout(
            polar=polar_config,
            showlegend=False,
        )

        # If theta='y', we need to swap how data is interpreted
        # This is complex in Plotly and may require trace transformation
        if self.theta == 'y':
            # For theta='y', radius is x and angle is y
            # This requires swapping the interpretation
            for trace in fig.data:
                if hasattr(trace, 'r') and hasattr(trace, 'theta'):
                    # Already polar trace, swap r and theta
                    r_data = trace.r
                    theta_data = trace.theta
                    trace.r = theta_data
                    trace.theta = r_data

        fig.update_traces(mode="lines")
