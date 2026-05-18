# geoms/geom_tile.py

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from ..aesthetic_mapper import map_continuous_colors
from ._geo_overlay import has_geo_context, infer_tile_polygons, tile_specs_to_geojson
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
        if has_geo_context(fig):
            self._draw_geo(fig, data)
            return

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

    def _draw_geo(self, fig, data):
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        geo_key = self.params.get("_geo_key")
        alpha = self.params.get("alpha", 1)

        if "fill" in self.mapping and self.mapping["fill"] in data.columns:
            fill_values = data[self.mapping["fill"]]
        else:
            fill_values = pd.Series(
                [self.params.get("fill", self.params.get("color", "#1f77b4"))] * len(data),
                index=data.index,
            )

        if pd.api.types.is_numeric_dtype(fill_values):
            colors = map_continuous_colors(
                fill_values,
                palette=self.params.get("palette", "Viridis"),
                default_color="#1f77b4",
            )
            specs = infer_tile_polygons(x, y, fill_values, colors)
            if not specs:
                return

            geojson, locations = tile_specs_to_geojson(specs)
            z_values = pd.to_numeric(fill_values, errors="coerce")
            trace = go.Choropleth(
                geojson=geojson,
                locations=locations,
                z=z_values,
                featureidkey="properties.id",
                colorscale=self.params.get("palette", "Viridis"),
                zmin=z_values.min(),
                zmax=z_values.max(),
                marker=dict(
                    line=dict(width=0),
                    opacity=alpha,
                ),
                showscale=True,
                colorbar=dict(title=self.params.get("name", self.mapping.get("fill", "fill"))),
                showlegend=False,
                hoverinfo="skip",
                name=self.params.get("name", "Tile"),
                meta={"_ggplotly_geo_tile": True},
            )
            if geo_key:
                trace.geo = geo_key
            fig.add_trace(trace)
            return
        else:
            categorical = pd.Categorical(fill_values)
            categories = list(categorical.categories)
            color_map = {
                val: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i, val in enumerate(categories)
            }
            colors = fill_values.map(color_map)
            specs = infer_tile_polygons(x, y, fill_values, colors)
            if not specs or not categories:
                return

            codes = pd.Series(categorical.codes, index=fill_values.index).mask(
                lambda values: values < 0
            )
            if len(categories) == 1:
                colorscale = [[0, color_map[categories[0]]], [1, color_map[categories[0]]]]
            else:
                colorscale = []
                for i, category in enumerate(categories):
                    start = i / len(categories)
                    end = (i + 1) / len(categories)
                    colorscale.extend([[start, color_map[category]], [end, color_map[category]]])

            geojson, locations = tile_specs_to_geojson(specs)
            trace = go.Choropleth(
                geojson=geojson,
                locations=locations,
                z=codes,
                featureidkey="properties.id",
                colorscale=colorscale,
                zmin=0,
                zmax=max(len(categories) - 1, 1),
                marker=dict(
                    line=dict(width=0),
                    opacity=alpha,
                ),
                showscale=False,
                showlegend=False,
                hoverinfo="skip",
                name=self.params.get("name", "Tile"),
                meta={"_ggplotly_geo_tile": True},
            )
            if geo_key:
                trace.geo = geo_key
            fig.add_trace(trace)
