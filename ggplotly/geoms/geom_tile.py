# geoms/geom_tile.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .geom_base import Geom


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

    required_aes = ['x', 'y']

    def _draw_impl(self, fig, data, row, col):
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        z = data[self.mapping["fill"]] if "fill" in self.mapping else None
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
                # Handle categorical fill as numeric codes with labeled colorbar.
                categorical = pd.Categorical(z)
                categories = list(categorical.categories)
                if not categories:
                    return

                color_map = {
                    val: px.colors.qualitative.Plotly[
                        i % len(px.colors.qualitative.Plotly)
                    ]
                    for i, val in enumerate(categories)
                }

                codes = pd.Series(categorical.codes, index=z.index)
                codes = codes.mask(codes < 0)
                if len(categories) == 1:
                    colorscale = [[0, color_map[categories[0]]], [1, color_map[categories[0]]]]
                else:
                    colorscale = []
                    for i, category in enumerate(categories):
                        start = i / len(categories)
                        end = (i + 1) / len(categories)
                        colorscale.extend([[start, color_map[category]], [end, color_map[category]]])

                fig.add_trace(
                    go.Heatmap(
                        x=x,
                        y=y,
                        z=codes,
                        zmin=0,
                        zmax=max(len(categories) - 1, 1),
                        colorscale=colorscale,
                        opacity=alpha,
                        name=self.params.get("name", "Tile"),
                        colorbar=dict(
                            title=self.params.get("name", "Tile"),
                            tickmode="array",
                            tickvals=list(range(len(categories))),
                            ticktext=[str(category) for category in categories],
                        ),
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
