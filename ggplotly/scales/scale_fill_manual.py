from .scale_base import Scale


class scale_fill_manual(Scale):
    """Scale for manually defining fill colors based on a categorical variable."""

    aesthetic = 'fill'

    def __init__(self, values, name=None, breaks=None, labels=None, na_value='gray',
                 aesthetics='fill', guide='legend'):
        """
        Manually define fill colors for each level of a categorical variable.

        Parameters
        ----------
        values : dict or list
            Dictionary mapping each level of the categorical variable to a color,
            or a list of colors to be matched to categories in order.
            Keys are the category values, values are color specifications
            (names, hex codes, or rgb strings).
        name : str, optional
            Title for the legend.
        breaks : list, optional
            A list specifying which categories should appear in the legend.
            By default, all categories are shown.
        labels : list, optional
            A list of labels corresponding to the breaks, to be shown in the legend.
            Must be the same length as breaks if provided.
        na_value : str, default='gray'
            Color to use for missing values or categories not in the mapping.
        aesthetics : str, default='fill'
            The name of the aesthetic that this scale works with.
        guide : str, default='legend'
            Type of legend to use. Options: 'legend', 'none'.

        Examples
        --------
        >>> scale_fill_manual({'A': 'red', 'B': 'blue', 'C': 'green'})
        >>> scale_fill_manual(['red', 'blue', 'green'])  # colors assigned in order
        >>> scale_fill_manual({'low': '#FEE08B', 'high': '#D73027'}, name='Level')
        >>> scale_fill_manual({'A': 'red', 'B': 'blue'}, breaks=['A'], labels=['Category A'])
        """
        self.values = values
        self.name = name
        self.breaks = breaks
        self.labels = labels
        self.na_value = na_value
        self.aesthetics = aesthetics
        self.guide = guide

    def apply_scale(self, data, mapping):
        """
        Applies the manual fill scale to the data.

        Parameters:
            data (DataFrame): The input data containing the fill aesthetic.
            mapping (dict): The mapping of the categorical variable to the fill color.

        Returns:
            DataFrame: Modified data with the manual fill color applied.
        """
        fill_variable = mapping.get("fill")
        if fill_variable is None or fill_variable not in data.columns:
            return data  # No fill aesthetic to modify

        # Handle list or dict values
        if isinstance(self.values, dict):
            color_map = self.values
        else:
            # Assume values is a list; map to unique categories in order
            categories = data[fill_variable].unique()
            color_map = dict(zip(categories, self.values))

        # Map the values to their corresponding colors
        data["fill"] = data[fill_variable].map(color_map).fillna(self.na_value)

        return data

    def apply(self, fig):
        """
        Apply the manual fill scale to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        self._apply_manual_color_mapping(
            fig, self.values, name=self.name,
            breaks=self.breaks, labels=self.labels,
            update_fill=True, guide=self.guide
        )

    def get_legend_info(self):
        """
        Returns the legend information (name and colors) for the manual fill scale.

        Returns:
            dict: Legend information including name and color mappings.
        """
        return {"name": self.name, "values": self.values, "breaks": self.breaks,
                "labels": self.labels}
