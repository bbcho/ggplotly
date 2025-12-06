from .scale_base import Scale

# scales/scale_color_brewer.py
import plotly.express as px


class scale_color_brewer(Scale):
    """Scale for mapping a categorical variable to a ColorBrewer palette."""

    def __init__(self, type="qual", palette="Set1"):
        """
        Map a categorical variable to a ColorBrewer palette for color aesthetic.

        Parameters
        ----------
        type : str, default='qual'
            Type of ColorBrewer palette:
            - 'qual': Qualitative (categorical data)
            - 'seq': Sequential (ordered data)
            - 'div': Diverging (data with meaningful midpoint)
        palette : str, default='Set1'
            Name of the ColorBrewer palette. Examples:
            - Qualitative: 'Set1', 'Set2', 'Set3', 'Pastel1', 'Dark2'
            - Sequential: 'Blues', 'Greens', 'Reds', 'Oranges', 'Purples'
            - Diverging: 'RdBu', 'RdYlGn', 'BrBG', 'PiYG'

        Examples
        --------
        >>> scale_color_brewer()  # default: Set1 qualitative
        >>> scale_color_brewer(type='seq', palette='Blues')
        >>> scale_color_brewer(type='div', palette='RdBu')
        """
        self.type = type
        self.palette = palette

    def apply_scale(self, data, mapping):
        """
        Applies the ColorBrewer palette to the data based on the categorical variable.

        Parameters:
            data (DataFrame): The input data containing the color aesthetic.
            mapping (dict): The mapping of the categorical variable to the color scale.

        Returns:
            DataFrame: Modified data with the color aesthetic applied.
        """
        color_variable = mapping.get("color")
        if color_variable is None or color_variable not in data.columns:
            return data  # No color aesthetic to modify

        # Define the available ColorBrewer palettes
        if self.type == "qual":
            color_palette = px.colors.qualitative.__dict__[self.palette]
        elif self.type == "seq":
            color_palette = px.colors.sequential.__dict__[self.palette]
        elif self.type == "div":
            color_palette = px.colors.diverging.__dict__[self.palette]
        else:
            raise ValueError(f"Unsupported type '{self.type}' for ColorBrewer scale.")

        # Apply the color palette to the categorical variable
        unique_values = data[color_variable].unique()
        color_map = {
            val: color_palette[i % len(color_palette)]
            for i, val in enumerate(unique_values)
        }
        data["color"] = data[color_variable].map(color_map)

        return data

    def get_legend_info(self):
        """
        Returns the legend information for the ColorBrewer scale.

        Returns:
            dict: Legend information with the color mapping.
        """
        return {"name": self.palette, "values": self.palette}
