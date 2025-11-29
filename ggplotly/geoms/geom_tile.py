# geoms/geom_tile.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_tile(Geom):
    """
    Geom for drawing tile plots (heatmaps).

    Automatically handles both continuous and categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        fill (str, optional): Fill color for the tiles.
        alpha (float, optional): Transparency level for the fill color. Default is 1.
        palette (str, optional): Color palette name for continuous fill. Default is 'Viridis'.
        group (str, optional): Grouping variable for the tiles.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        z = data[self.mapping["fill"]] if "fill" in self.mapping else None
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        alpha = self.params.get("alpha", 1)

        # Handle fill mapping if fill is categorical or continuous
        if z is not None:
            if pd.api.types.is_numeric_dtype(z):
                # Handle continuous fill with a gradient color scale (e.g., for heatmaps)
                fig.add_trace(
                    go.Heatmap(
                        x=x,
                        y=y,
                        z=z,
                        colorscale=self.params.get("palette", "Viridis"),
                        opacity=alpha,
                        colorbar=dict(title=self.params.get("name", "Intensity")),
                    ),
                    row=row,
                    col=col,
                )
            else:
                # Handle categorical fill (converts to color map)
                if not pd.api.types.is_categorical_dtype(z):
                    data[self.mapping["fill"]] = pd.Categorical(z)
                    z = data[self.mapping["fill"]]

                unique_colors = z.unique()
                color_map = {
                    val: px.colors.qualitative.Plotly[
                        i % len(px.colors.qualitative.Plotly)
                    ]
                    for i, val in enumerate(unique_colors)
                }
                z = z.map(color_map)

                fig.add_trace(
                    go.Heatmap(
                        x=x,
                        y=y,
                        z=None,  # z is ignored in case of categorical values
                        colorscale=[(0, color_map[val]) for val in unique_colors],
                        opacity=alpha,
                        name=self.params.get("name", "Tile"),
                    ),
                    row=row,
                    col=col,
                )
        else:
            fig.add_trace(
                go.Heatmap(
                    x=x,
                    y=y,
                    z=z,
                    colorscale="Viridis",
                    opacity=alpha,
                    name=self.params.get("name", "Tile"),
                ),
                row=row,
                col=col,
            )
