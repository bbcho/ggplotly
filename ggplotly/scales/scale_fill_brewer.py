from .scale_base import Scale

# scales/scale_fill_brewer.py
import plotly.express as px


class scale_fill_brewer(Scale):
    """
    Scale for mapping a categorical variable to a ColorBrewer palette for fill aesthetic.

    Parameters:
        type (str): The type of ColorBrewer palette ('qual', 'seq', 'div').
        palette (str): The name of the ColorBrewer palette.
    """

    def __init__(self, type="qual", palette="Set1"):
        self.type = type
        self.palette = palette

    def apply_scale(self, data, mapping):
        """
        Applies the ColorBrewer palette to the data based on the categorical variable.

        Parameters:
            data (DataFrame): The input data containing the fill aesthetic.
            mapping (dict): The mapping of the categorical variable to the fill scale.

        Returns:
            DataFrame: Modified data with the fill aesthetic applied.
        """
        fill_variable = mapping.get("fill")
        if fill_variable is None or fill_variable not in data.columns:
            return data  # No fill aesthetic to modify

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
        unique_values = data[fill_variable].unique()
        color_map = {
            val: color_palette[i % len(color_palette)]
            for i, val in enumerate(unique_values)
        }
        data["fill"] = data[fill_variable].map(color_map)

        return data

    def get_legend_info(self):
        """
        Returns the legend information for the ColorBrewer scale.

        Returns:
            dict: Legend information with the color mapping.
        """
        return {"name": self.palette, "values": self.palette}
