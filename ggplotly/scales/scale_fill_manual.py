from .scale_base import Scale


class scale_fill_manual(Scale):
    """Scale for manually defining fill colors based on a categorical variable."""

    def __init__(self, values, name=None):
        """
        Manually define fill colors for each level of a categorical variable.

        Parameters
        ----------
        values : dict
            Dictionary mapping each level of the categorical variable to a color.
            Keys are the category values, values are color specifications
            (names, hex codes, or rgb strings).
        name : str, optional
            Title for the legend.

        Examples
        --------
        >>> scale_fill_manual({'A': 'red', 'B': 'blue', 'C': 'green'})
        >>> scale_fill_manual({'low': '#FEE08B', 'high': '#D73027'}, name='Level')
        """
        self.values = values
        self.name = name

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

        # Map the values to their corresponding colors
        data["fill"] = (
            data[fill_variable].map(self.values).fillna("gray")
        )  # Default to 'gray' if no match

        return data

    def get_legend_info(self):
        """
        Returns the legend information (name and colors) for the manual fill scale.

        Returns:
            dict: Legend information including name and color mappings.
        """
        return {"name": self.name, "values": self.values}
