from .scale_base import Scale

# scales/scale_color_brewer.py
import plotly.express as px


class scale_color_brewer(Scale):
    """Scale for mapping a categorical variable to a ColorBrewer palette."""

    def __init__(self, type="seq", palette=1, direction=1):
        """
        Map a categorical variable to a ColorBrewer palette for color aesthetic.

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
        >>> scale_color_brewer()  # default: sequential palette
        >>> scale_color_brewer(type='qual', palette='Set1')
        >>> scale_color_brewer(type='div', palette='RdBu')
        >>> scale_color_brewer(palette='Blues', direction=-1)  # reversed
        """
        self.direction = direction

        # Handle palette as integer index or string name
        if isinstance(palette, int):
            # Map integer to palette name based on type
            self.palette = self._get_palette_by_index(type, palette)
            self.type = type
        else:
            self.palette = palette
            # Auto-detect type from palette name if type not explicitly set
            self.type = self._infer_palette_type(palette) if type == "seq" else type

    def _infer_palette_type(self, palette):
        """Infer the palette type from the palette name."""
        # Qualitative palettes
        qual_palettes = ['Accent', 'Dark2', 'Paired', 'Pastel1', 'Pastel2',
                         'Set1', 'Set2', 'Set3']
        # Diverging palettes
        div_palettes = ['BrBG', 'PiYG', 'PRGn', 'PuOr', 'RdBu', 'RdGy',
                        'RdYlBu', 'RdYlGn', 'Spectral']

        if palette in qual_palettes:
            return 'qual'
        elif palette in div_palettes:
            return 'div'
        else:
            return 'seq'

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

    def _get_color_palette(self):
        """Get the color palette based on type and palette name."""
        # Map ColorBrewer palette names to Plotly equivalents
        # Some ColorBrewer palettes don't exist in Plotly, so we use similar alternatives
        palette_mapping = {
            'Accent': 'Vivid',  # Both are qualitative with distinct colors
            'Paired': 'D3',     # Both have paired-style colors
        }
        palette_name = palette_mapping.get(self.palette, self.palette)

        try:
            if self.type == "qual":
                color_palette = getattr(px.colors.qualitative, palette_name)
            elif self.type == "seq":
                color_palette = getattr(px.colors.sequential, palette_name)
            elif self.type == "div":
                color_palette = getattr(px.colors.diverging, palette_name)
            else:
                raise ValueError(f"Unsupported type '{self.type}' for ColorBrewer scale.")
        except AttributeError:
            raise ValueError(f"Palette '{self.palette}' not found for type '{self.type}'")

        # Reverse palette if direction is -1
        if self.direction == -1:
            color_palette = list(reversed(color_palette))

        return color_palette

    def apply(self, fig):
        """
        Apply the ColorBrewer color scale to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        color_palette = self._get_color_palette()

        # Extract categories from trace names
        categories = []
        for trace in fig.data:
            if hasattr(trace, 'name') and trace.name and trace.name not in categories:
                categories.append(trace.name)

        # Create color mapping
        color_map = {
            cat: color_palette[i % len(color_palette)]
            for i, cat in enumerate(categories)
        }

        # Apply colors to traces
        for trace in fig.data:
            if hasattr(trace, 'name') and trace.name in color_map:
                color = color_map[trace.name]
                if hasattr(trace, 'marker') and trace.marker is not None:
                    trace.marker.color = color
                if hasattr(trace, 'line') and trace.line is not None:
                    trace.line.color = color
                if hasattr(trace, 'fillcolor'):
                    trace.fillcolor = color

    def get_legend_info(self):
        """
        Returns the legend information for the ColorBrewer scale.

        Returns:
            dict: Legend information with the color mapping.
        """
        return {"name": self.palette, "values": self.palette}
