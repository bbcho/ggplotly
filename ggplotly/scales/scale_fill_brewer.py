from .scale_base import Scale

# scales/scale_fill_brewer.py
import plotly.express as px


class scale_fill_brewer(Scale):
    """Scale for mapping a categorical variable to a ColorBrewer palette for fill aesthetic."""

    def __init__(self, type="seq", palette=1, direction=1):
        """
        Map a categorical variable to a ColorBrewer palette for fill aesthetic.

        Parameters
        ----------
        type : str, default='seq'
            Type of ColorBrewer palette:
            - 'seq': Sequential (ordered data) - default to match R
            - 'qual': Qualitative (categorical data)
            - 'div': Diverging (data with meaningful midpoint)
        palette : int or str, default=1
            Index or name of the ColorBrewer palette. Can be:
            - An integer index (1-based, to match R)
            - A string name like 'Blues', 'Set1', 'RdBu'
            Common palette names:
            - Sequential: 'Blues', 'Greens', 'Reds', 'Oranges', 'Purples'
            - Qualitative: 'Set1', 'Set2', 'Set3', 'Pastel1', 'Dark2'
            - Diverging: 'RdBu', 'RdYlGn', 'BrBG', 'PiYG'
        direction : int, default=1
            Direction of the palette. 1 for normal order, -1 for reversed.

        Examples
        --------
        >>> scale_fill_brewer()  # default: sequential palette
        >>> scale_fill_brewer(type='qual', palette='Set1')
        >>> scale_fill_brewer(type='div', palette='RdBu')
        >>> scale_fill_brewer(palette='Blues', direction=-1)  # reversed
        """
        self.type = type
        self.direction = direction

        # Handle palette as integer index or string name
        if isinstance(palette, int):
            # Map integer to palette name based on type
            self.palette = self._get_palette_by_index(type, palette)
        else:
            self.palette = palette

    def _get_palette_by_index(self, type, index):
        """Get palette name from index (1-based to match R)."""
        # Default palettes by type, ordered to match R's brewer.pal.info
        seq_palettes = ['Blues', 'BuGn', 'BuPu', 'GnBu', 'Greens', 'Greys',
                        'Oranges', 'OrRd', 'PuBu', 'PuBuGn', 'PuRd', 'Purples',
                        'RdPu', 'Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']
        qual_palettes = ['Accent', 'Dark2', 'Paired', 'Pastel1', 'Pastel2',
                         'Set1', 'Set2', 'Set3']
        div_palettes = ['BrBG', 'PiYG', 'PRGn', 'PuOr', 'RdBu', 'RdGy',
                        'RdYlBu', 'RdYlGn', 'Spectral']

        palettes = {'seq': seq_palettes, 'qual': qual_palettes, 'div': div_palettes}
        palette_list = palettes.get(type, seq_palettes)

        # Convert 1-based index to 0-based, with bounds checking
        idx = max(0, min(index - 1, len(palette_list) - 1))
        return palette_list[idx]

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

        # Reverse palette if direction is -1
        if self.direction == -1:
            color_palette = list(reversed(color_palette))

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
