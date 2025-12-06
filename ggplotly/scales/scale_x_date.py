# scales/scale_x_date.py

from .scale_base import Scale


class scale_x_date(Scale):
    """Date scale for the x-axis."""

    def __init__(
        self,
        name=None,
        limits=None,
        date_breaks=None,
        date_labels=None,
        breaks=None,
        labels=None,
        expand=None,
    ):
        """
        Format date values on the x-axis with customizable breaks and labels.

        Similar to ggplot2's scale_x_date().

        Parameters
        ----------
        name : str, optional
            Label for the x-axis.
        limits : tuple, optional
            Two-element tuple specifying date limits (min, max).
            Can be date strings ('2020-01-01') or datetime objects.
        date_breaks : str, optional
            Interval for tick marks. Examples:
            '1 day', '2 weeks', '1 month', '3 months', '1 year'.
        date_labels : str, optional
            strftime format string for tick labels. Examples:
            '%Y' (2020), '%b %Y' (Jan 2020), '%Y-%m-%d' (2020-01-15).
        breaks : list, optional
            Explicit list of date positions for ticks.
        labels : list, optional
            Explicit list of labels corresponding to breaks.
        expand : tuple, optional
            Expansion to add to limits (mult, add). Default (0.05, 0).

        Examples
        --------
        >>> scale_x_date(date_breaks='1 month', date_labels='%b %Y')
        >>> scale_x_date(limits=('2020-01-01', '2023-12-31'), date_breaks='6 months')
        """
        self.name = name
        self.limits = limits
        self.date_breaks = date_breaks
        self.date_labels = date_labels
        self.breaks = breaks
        self.labels = labels
        self.expand = expand

    def _parse_date_breaks(self, date_breaks):
        """
        Parse date_breaks string like '1 month' or '2 weeks' into Plotly dtick format.

        Returns:
            tuple: (dtick_value, dtick_unit) for Plotly
        """
        if date_breaks is None:
            return None

        parts = date_breaks.lower().strip().split()
        if len(parts) == 1:
            # Just the unit, assume 1
            num = 1
            unit = parts[0]
        elif len(parts) == 2:
            num = int(parts[0])
            unit = parts[1]
        else:
            raise ValueError(f"Invalid date_breaks format: {date_breaks}")

        # Remove trailing 's' if present (months -> month)
        if unit.endswith('s'):
            unit = unit[:-1]

        # Convert to Plotly dtick format
        # Plotly uses milliseconds for dtick with date axes
        if unit in ('day', 'd'):
            return num * 24 * 60 * 60 * 1000  # milliseconds in a day
        elif unit in ('week', 'w'):
            return num * 7 * 24 * 60 * 60 * 1000
        elif unit in ('month', 'mo', 'm'):
            # Plotly uses 'M1', 'M3', etc. for months
            return f"M{num}"
        elif unit in ('year', 'y'):
            return f"M{num * 12}"
        elif unit in ('quarter', 'q'):
            return f"M{num * 3}"
        else:
            raise ValueError(f"Unknown date unit: {unit}")

    def apply(self, fig):
        """
        Apply the date scale to the x-axis.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        xaxis_update = {"type": "date"}

        if self.name is not None:
            xaxis_update["title_text"] = self.name

        if self.limits is not None:
            xaxis_update["range"] = list(self.limits)

        # Handle date_breaks
        if self.date_breaks is not None:
            dtick = self._parse_date_breaks(self.date_breaks)
            xaxis_update["dtick"] = dtick

        # Handle date_labels (strftime format)
        if self.date_labels is not None:
            xaxis_update["tickformat"] = self.date_labels

        # Handle explicit breaks
        if self.breaks is not None:
            xaxis_update["tickmode"] = "array"
            xaxis_update["tickvals"] = self.breaks
            if self.labels is not None:
                xaxis_update["ticktext"] = self.labels

        fig.update_xaxes(**xaxis_update)


class scale_x_datetime(scale_x_date):
    """Datetime scale for the x-axis with time component support."""

    def __init__(
        self,
        name=None,
        limits=None,
        date_breaks=None,
        date_labels=None,
        breaks=None,
        labels=None,
        expand=None,
    ):
        """
        Format datetime values on the x-axis with time component support.

        Like scale_x_date but for datetime data with time components.
        Supports finer granularity like hours, minutes, seconds.

        Parameters
        ----------
        name : str, optional
            Label for the x-axis.
        limits : tuple, optional
            Two-element tuple specifying datetime limits.
        date_breaks : str, optional
            Interval for tick marks. Examples:
            '1 hour', '6 hours', '1 day', '1 week'.
        date_labels : str, optional
            strftime format string. Examples:
            '%Y-%m-%d %H:%M' (full), '%H:%M' (time only).
        breaks : list, optional
            Explicit list of datetime positions for ticks.
        labels : list, optional
            Explicit list of labels corresponding to breaks.
        expand : tuple, optional
            Expansion to add to limits.

        Examples
        --------
        >>> scale_x_datetime(date_breaks='1 hour', date_labels='%H:%M')
        >>> scale_x_datetime(date_breaks='1 day', date_labels='%b %d')
        """
        super().__init__(name, limits, date_breaks, date_labels, breaks, labels, expand)

    def _parse_date_breaks(self, date_breaks):
        """
        Parse date_breaks string including time units.
        """
        if date_breaks is None:
            return None

        parts = date_breaks.lower().strip().split()
        if len(parts) == 1:
            num = 1
            unit = parts[0]
        elif len(parts) == 2:
            num = int(parts[0])
            unit = parts[1]
        else:
            raise ValueError(f"Invalid date_breaks format: {date_breaks}")

        if unit.endswith('s'):
            unit = unit[:-1]

        # Time units (in milliseconds)
        if unit in ('second', 'sec', 's'):
            return num * 1000
        elif unit in ('minute', 'min'):
            return num * 60 * 1000
        elif unit in ('hour', 'hr', 'h'):
            return num * 60 * 60 * 1000
        else:
            # Fall back to parent implementation for day/week/month/year
            return super()._parse_date_breaks(date_breaks)
