# pytest/test_geom_edgebundle.py
"""
Comprehensive test suite for geom_edgebundle, stat_edgebundle, and map theme styling.
"""

import numpy as np
import pandas as pd

import pytest
from ggplotly import (
    aes,
    geom_edgebundle,
    geom_map,
    geom_point,
    ggplot,
    labs,
    theme_bbc,
    theme_classic,
    theme_dark,
    theme_default,
    theme_ggplot2,
    theme_minimal,
    theme_nytimes,
)
from ggplotly.stats.stat_edgebundle import stat_edgebundle


class TestStatEdgebundle:
    """Tests for the stat_edgebundle statistical transformation."""

    def test_basic_bundling(self):
        """Test that basic bundling produces output."""
        edges_df = pd.DataFrame({
            'x': [0, 0, 0],
            'y': [0, 0.3, 0.6],
            'xend': [10, 10, 10],
            'yend': [0, 0.3, 0.6]
        })

        stat = stat_edgebundle(C=2, I=10, verbose=False)
        bundled = stat.compute(edges_df)

        assert len(bundled) > 0
        assert 'x' in bundled.columns
        assert 'y' in bundled.columns
        assert 'group' in bundled.columns
        assert 'index' in bundled.columns

    def test_output_structure(self):
        """Test that output has correct structure."""
        edges_df = pd.DataFrame({
            'x': [0, 1],
            'y': [0, 1],
            'xend': [5, 6],
            'yend': [5, 6]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)
        bundled = stat.compute(edges_df)

        # Should have 2 groups (one per edge)
        assert bundled['group'].nunique() == 2

        # Index should be in [0, 1]
        assert bundled['index'].min() >= 0.0
        assert bundled['index'].max() <= 1.0

        # All edges should have same number of points
        counts = bundled.groupby('group').size()
        assert len(counts.unique()) == 1

    def test_endpoint_preservation(self):
        """Test that endpoints are preserved after bundling."""
        edges_df = pd.DataFrame({
            'x': [0, 5],
            'y': [0, 5],
            'xend': [10, 15],
            'yend': [10, 15]
        })

        stat = stat_edgebundle(C=2, I=10, verbose=False)
        bundled = stat.compute(edges_df)

        for i in range(2):
            edge_data = bundled[bundled['group'] == i]
            first = edge_data.iloc[0]
            last = edge_data.iloc[-1]

            # Check start point
            assert abs(first['x'] - edges_df.iloc[i]['x']) < 1e-5
            assert abs(first['y'] - edges_df.iloc[i]['y']) < 1e-5

            # Check end point
            assert abs(last['x'] - edges_df.iloc[i]['xend']) < 1e-5
            assert abs(last['y'] - edges_df.iloc[i]['yend']) < 1e-5

    def test_parallel_edges_bundle(self):
        """Test that parallel edges bundle together."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 0.5],
            'xend': [10, 10],
            'yend': [0, 0.5]
        })

        stat = stat_edgebundle(C=3, I=20, compatibility_threshold=0.6, verbose=False)
        bundled = stat.compute(edges_df)

        # Get middle points
        edge0 = bundled[bundled['group'] == 0]
        edge1 = bundled[bundled['group'] == 1]

        mid_idx0 = (edge0['index'] - 0.5).abs().argmin()
        mid_idx1 = (edge1['index'] - 0.5).abs().argmin()

        edge0_mid = edge0.iloc[mid_idx0]
        edge1_mid = edge1.iloc[mid_idx1]

        # Distance between midpoints should be less than original 0.5
        distance = np.sqrt((edge0_mid['x'] - edge1_mid['x'])**2 +
                          (edge0_mid['y'] - edge1_mid['y'])**2)

        assert distance < 0.4, f"Parallel edges should bundle closer, got distance {distance}"

    def test_perpendicular_edges_dont_bundle(self):
        """Test that perpendicular edges don't bundle."""
        edges_df = pd.DataFrame({
            'x': [0, 5],
            'y': [5, 0],
            'xend': [10, 5],
            'yend': [5, 10]
        })

        stat = stat_edgebundle(C=3, I=20, compatibility_threshold=0.6, verbose=False)
        bundled = stat.compute(edges_df)

        # Horizontal edge should stay mostly horizontal
        edge0 = bundled[bundled['group'] == 0]
        y_std = edge0['y'].std()
        assert y_std < 1.0, f"Horizontal edge bent too much: y_std={y_std}"

        # Vertical edge should stay mostly vertical
        edge1 = bundled[bundled['group'] == 1]
        x_std = edge1['x'].std()
        assert x_std < 1.0, f"Vertical edge bent too much: x_std={x_std}"

    def test_missing_columns_error(self):
        """Test that missing columns raise an error."""
        edges_df = pd.DataFrame({
            'x': [0, 1],
            'y': [0, 1]
            # Missing xend, yend
        })

        stat = stat_edgebundle(verbose=False)

        with pytest.raises(ValueError, match="Missing required columns"):
            stat.compute(edges_df)

    def test_single_edge(self):
        """Test bundling with a single edge."""
        edges_df = pd.DataFrame({
            'x': [0],
            'y': [0],
            'xend': [10],
            'yend': [10]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)
        bundled = stat.compute(edges_df)

        assert bundled['group'].nunique() == 1
        assert len(bundled) > 2  # Should have subdivision points


class TestGeomEdgebundle:
    """Tests for geom_edgebundle."""

    def test_basic_plot(self):
        """Test basic edge bundle plot creation."""
        edges_df = pd.DataFrame({
            'x': [0, 0, 0],
            'y': [0, 1, 2],
            'xend': [10, 10, 10],
            'yend': [0, 1, 2]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=2, I=5, verbose=False)
        ).draw()

        # Should have traces (bundles + highlights)
        assert len(fig.data) > 0
        assert fig.data[0].type == 'scatter'

    def test_custom_colors(self):
        """Test custom color parameter."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(color='blue', alpha=0.5, C=2, I=5, verbose=False,
                             show_highlight=False)
        ).draw()

        # Check that color was applied (rgba format)
        assert 'rgba(0,0,255,0.5)' in fig.data[0].line.color

    def test_with_points(self):
        """Test edge bundles with points overlay."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        nodes_df = pd.DataFrame({
            'x': [0, 0, 10, 10],
            'y': [0, 1, 0, 1]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=2, I=5, verbose=False, show_highlight=False)
            + geom_point(data=nodes_df, mapping=aes(x='x', y='y'), size=5)
        ).draw()

        # Should have edge traces + point trace
        trace_types = [t.type for t in fig.data]
        assert 'scatter' in trace_types

    def test_no_highlight(self):
        """Test disabling highlight lines."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=2, I=5, verbose=False, show_highlight=False)
        ).draw()

        # Count traces - should be 2 (one per edge, no highlights)
        assert len(fig.data) == 2

    def test_with_highlight(self):
        """Test enabling highlight lines doubles trace count."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=2, I=5, verbose=False, show_highlight=True)
        ).draw()

        # Count traces - should be 4 (2 edges + 2 highlights)
        assert len(fig.data) == 4

    def test_with_theme(self):
        """Test edge bundles with theme."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=2, I=5, verbose=False)
            + theme_dark()
            + labs(title='Edge Bundle Test')
        ).draw()

        assert fig.layout.title.text == 'Edge Bundle Test'

    def test_empty_data(self):
        """Test handling of empty data."""
        edges_df = pd.DataFrame({
            'x': [],
            'y': [],
            'xend': [],
            'yend': []
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=2, I=5, verbose=False)
        ).draw()

        # Should not crash, may have no data traces
        assert fig is not None


class TestGeoContextDetection:
    """Tests for geographic context detection."""

    def test_cartesian_mode_default(self):
        """Test that default mode is Cartesian (Scatter traces)."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=2, I=5, verbose=False, show_highlight=False)
        ).draw()

        # Should use Scatter, not Scattergeo
        assert fig.data[0].type == 'scatter'

    def test_geo_mode_with_geom_map(self):
        """Test that geo mode is detected when geom_map is present."""
        # Create airports (nodes)
        airports_df = pd.DataFrame({
            'lon': [-122.4, -73.8, -87.6],
            'lat': [37.8, 40.6, 41.9],
            'name': ['SFO', 'JFK', 'ORD']
        })

        # Create flights (edges)
        flights_df = pd.DataFrame({
            'src_lon': [-122.4, -73.8],
            'src_lat': [37.8, 40.6],
            'dst_lon': [-73.8, -87.6],
            'dst_lat': [40.6, 41.9]
        })

        fig = (
            ggplot(flights_df, aes(x='src_lon', y='src_lat', xend='dst_lon', yend='dst_lat'))
            + geom_map(map_type='usa')
            + geom_point(data=airports_df, mapping=aes(x='lon', y='lat'))
            + geom_edgebundle(C=2, I=5, verbose=False, show_highlight=False)
        ).draw()

        # Should have Scattergeo traces
        trace_types = [t.type for t in fig.data]
        assert 'scattergeo' in trace_types


class TestBundlingParameters:
    """Tests for bundling parameter effects."""

    def test_compatibility_threshold_effect(self):
        """Test that compatibility threshold affects bundling."""
        edges_df = pd.DataFrame({
            'x': [0, 0, 0],
            'y': [0, 1, 2],
            'xend': [10, 10, 10],
            'yend': [0, 1, 2]
        })

        # Low threshold - more bundling
        stat_low = stat_edgebundle(C=3, I=20, compatibility_threshold=0.3, verbose=False)
        bundled_low = stat_low.compute(edges_df)

        # High threshold - less bundling
        stat_high = stat_edgebundle(C=3, I=20, compatibility_threshold=0.9, verbose=False)
        bundled_high = stat_high.compute(edges_df)

        # Both should produce valid output
        assert len(bundled_low) > 0
        assert len(bundled_high) > 0

    def test_cycles_effect(self):
        """Test that more cycles produce more subdivision points."""
        edges_df = pd.DataFrame({
            'x': [0],
            'y': [0],
            'xend': [10],
            'yend': [10]
        })

        stat_few = stat_edgebundle(C=2, I=5, verbose=False)
        bundled_few = stat_few.compute(edges_df)

        stat_many = stat_edgebundle(C=4, I=5, verbose=False)
        bundled_many = stat_many.compute(edges_df)

        # More cycles = more subdivision points
        assert len(bundled_many) > len(bundled_few)


class TestRealWorldScenarios:
    """Tests simulating real-world usage patterns."""

    def test_network_graph(self):
        """Test edge bundling on a small network graph."""
        # Create a simple network
        np.random.seed(42)
        n_nodes = 10
        n_edges = 15

        # Random node positions
        node_x = np.random.uniform(0, 100, n_nodes)
        node_y = np.random.uniform(0, 100, n_nodes)

        # Random edges
        edges = []
        for _ in range(n_edges):
            i, j = np.random.choice(n_nodes, 2, replace=False)
            edges.append({
                'x': node_x[i],
                'y': node_y[i],
                'xend': node_x[j],
                'yend': node_y[j]
            })

        edges_df = pd.DataFrame(edges)
        nodes_df = pd.DataFrame({'x': node_x, 'y': node_y})

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=3, I=20, verbose=False)
            + geom_point(data=nodes_df, mapping=aes(x='x', y='y'), size=8, color='white')
            + theme_dark()
        ).draw()

        assert len(fig.data) > 0

    def test_circular_layout(self):
        """Test edge bundling on circular layout."""
        n_nodes = 12
        angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
        radius = 10

        node_x = radius * np.cos(angles)
        node_y = radius * np.sin(angles)

        # Create edges from each node to node+4 (mod n)
        edges = []
        for i in range(n_nodes):
            j = (i + 4) % n_nodes
            edges.append({
                'x': node_x[i],
                'y': node_y[i],
                'xend': node_x[j],
                'yend': node_y[j]
            })

        edges_df = pd.DataFrame(edges)

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=4, I=30, compatibility_threshold=0.6, verbose=False)
        ).draw()

        assert len(fig.data) > 0


class TestHighlightCustomization:
    """Tests for highlight color and alpha customization."""

    def test_custom_highlight_color(self):
        """Test custom highlight color parameter."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(
                C=2, I=5, verbose=False,
                show_highlight=True,
                highlight_color='red',
                highlight_alpha=0.5
            )
        ).draw()

        # Should have 4 traces (2 edges + 2 highlights)
        assert len(fig.data) == 4

        # Last 2 traces should be highlights with red color
        highlight_trace = fig.data[-1]
        assert 'rgba(255,0,0,0.5)' in highlight_trace.line.color

    def test_highlight_hex_color(self):
        """Test highlight with hex color."""
        edges_df = pd.DataFrame({
            'x': [0],
            'y': [0],
            'xend': [10],
            'yend': [10]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(
                C=2, I=5, verbose=False,
                show_highlight=True,
                highlight_color='#00ff00',
                highlight_alpha=0.4
            )
        ).draw()

        # Check highlight trace has correct color
        highlight_trace = fig.data[-1]
        assert 'rgba(0,255,0,0.4)' in highlight_trace.line.color

    def test_highlight_width(self):
        """Test custom highlight width."""
        edges_df = pd.DataFrame({
            'x': [0],
            'y': [0],
            'xend': [10],
            'yend': [10]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(
                C=2, I=5, verbose=False,
                show_highlight=True,
                highlight_width=0.5
            )
        ).draw()

        # Check highlight trace has correct width
        highlight_trace = fig.data[-1]
        assert highlight_trace.line.width == 0.5

    def test_main_edge_linewidth(self):
        """Test main edge linewidth parameter."""
        edges_df = pd.DataFrame({
            'x': [0],
            'y': [0],
            'xend': [10],
            'yend': [10]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(
                C=2, I=5, verbose=False,
                show_highlight=False,
                linewidth=2.0
            )
        ).draw()

        # Check main trace has correct width
        assert fig.data[0].line.width == 2.0


class TestGeomMapStyling:
    """Tests for geom_map color parameters."""

    def test_default_map_colors(self):
        """Test that default map colors are applied."""
        airports_df = pd.DataFrame({
            'lon': [-122.4, -73.8],
            'lat': [37.8, 40.6]
        })

        fig = (
            ggplot(airports_df, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
        ).draw()

        # Should have geo layout
        assert fig.layout.geo is not None
        # Default land color should be light
        assert fig.layout.geo.landcolor == 'rgb(243, 243, 243)'

    def test_custom_map_colors(self):
        """Test custom map color parameters."""
        airports_df = pd.DataFrame({
            'lon': [-122.4, -73.8],
            'lat': [37.8, 40.6]
        })

        fig = (
            ggplot(airports_df, aes(x='lon', y='lat'))
            + geom_map(
                map_type='usa',
                landcolor='#333333',
                oceancolor='#111111',
                bgcolor='black',
                countrycolor='#666666'
            )
            + geom_point()
        ).draw()

        assert fig.layout.geo.landcolor == '#333333'
        assert fig.layout.geo.oceancolor == '#111111'
        assert fig.layout.geo.bgcolor == 'black'
        assert fig.layout.geo.countrycolor == '#666666'

    def test_map_subunit_color(self):
        """Test subunit (state borders) color."""
        airports_df = pd.DataFrame({
            'lon': [-122.4],
            'lat': [37.8]
        })

        fig = (
            ggplot(airports_df, aes(x='lon', y='lat'))
            + geom_map(
                map_type='usa',
                subunitcolor='#aaaaaa'
            )
            + geom_point()
        ).draw()

        assert fig.layout.geo.subunitcolor == '#aaaaaa'


class TestMapThemeStyling:
    """Tests for theme styling on geographic maps."""

    @pytest.fixture
    def geo_figure(self):
        """Create a basic geo figure for testing."""
        airports_df = pd.DataFrame({
            'lon': [-122.4, -73.8, -87.6],
            'lat': [37.8, 40.6, 41.9]
        })
        return airports_df

    def test_theme_dark_geo_styling(self, geo_figure):
        """Test that theme_dark applies dark geo styling."""
        fig = (
            ggplot(geo_figure, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + theme_dark()
        ).draw()

        # Dark theme should override default colors
        assert fig.layout.geo.bgcolor == 'rgb(17, 17, 17)'
        assert fig.layout.geo.landcolor == 'rgb(40, 40, 40)'
        assert fig.layout.geo.oceancolor == 'rgb(17, 17, 17)'

    def test_theme_classic_geo_styling(self, geo_figure):
        """Test that theme_classic applies classic geo styling."""
        fig = (
            ggplot(geo_figure, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + theme_classic()
        ).draw()

        assert fig.layout.geo.bgcolor == 'white'
        assert fig.layout.geo.landcolor == 'rgb(243, 243, 243)'

    def test_theme_minimal_geo_styling(self, geo_figure):
        """Test that theme_minimal applies minimal geo styling."""
        fig = (
            ggplot(geo_figure, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + theme_minimal()
        ).draw()

        assert fig.layout.geo.bgcolor == 'white'
        assert fig.layout.geo.landcolor == '#FAFAFA'

    def test_theme_ggplot2_geo_styling(self, geo_figure):
        """Test that theme_ggplot2 applies ggplot2-style geo styling."""
        fig = (
            ggplot(geo_figure, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + theme_ggplot2()
        ).draw()

        assert fig.layout.geo.bgcolor == '#E5E5E5'
        assert fig.layout.geo.landcolor == '#FFFFFF'

    def test_theme_nytimes_geo_styling(self, geo_figure):
        """Test that theme_nytimes applies NYT-style geo styling."""
        fig = (
            ggplot(geo_figure, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + theme_nytimes()
        ).draw()

        assert fig.layout.geo.bgcolor == 'white'
        assert fig.layout.geo.landcolor == '#F5F5F5'

    def test_theme_bbc_geo_styling(self, geo_figure):
        """Test that theme_bbc applies BBC-style geo styling."""
        fig = (
            ggplot(geo_figure, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + theme_bbc()
        ).draw()

        assert fig.layout.geo.bgcolor == '#FFFFFF'
        assert fig.layout.geo.landcolor == '#F0F0F0'

    def test_theme_default_geo_styling(self, geo_figure):
        """Test that theme_default applies default geo styling."""
        fig = (
            ggplot(geo_figure, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + theme_default()
        ).draw()

        assert fig.layout.geo.bgcolor == 'white'
        assert fig.layout.geo.landcolor == 'rgb(243, 243, 243)'

    def test_theme_does_not_affect_non_geo(self):
        """Test that theme geo styling only applies to geo figures."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 4, 9]})

        fig = (
            ggplot(df, aes(x='x', y='y'))
            + geom_point()
            + theme_dark()
        ).draw()

        # Non-geo figure should not have geo layout settings applied
        # (geo attribute may exist but not be configured)
        assert fig.data[0].type == 'scatter'


class TestEdgebundleWithMapThemes:
    """Tests for edge bundling combined with map themes."""

    def test_edgebundle_with_dark_theme_on_map(self):
        """Test edge bundling on map with dark theme."""
        airports_df = pd.DataFrame({
            'lon': [-122.4, -73.8, -87.6],
            'lat': [37.8, 40.6, 41.9]
        })

        flights_df = pd.DataFrame({
            'src_lon': [-122.4, -73.8],
            'src_lat': [37.8, 40.6],
            'dst_lon': [-73.8, -87.6],
            'dst_lat': [40.6, 41.9]
        })

        fig = (
            ggplot(flights_df, aes(x='src_lon', y='src_lat', xend='dst_lon', yend='dst_lat'))
            + geom_map(map_type='usa')
            + geom_point(data=airports_df, mapping=aes(x='lon', y='lat'))
            + geom_edgebundle(C=2, I=5, verbose=False, show_highlight=False)
            + theme_dark()
        ).draw()

        # Verify dark theme is applied to geo
        assert fig.layout.geo.bgcolor == 'rgb(17, 17, 17)'
        assert fig.layout.geo.landcolor == 'rgb(40, 40, 40)'

        # Verify edge bundles are Scattergeo
        geo_traces = [t for t in fig.data if t.type == 'scattergeo']
        assert len(geo_traces) > 0

    def test_edgebundle_with_custom_highlight_on_map(self):
        """Test edge bundling with custom highlights on map."""
        airports_df = pd.DataFrame({
            'lon': [-122.4, -73.8],
            'lat': [37.8, 40.6]
        })

        flights_df = pd.DataFrame({
            'src_lon': [-122.4],
            'src_lat': [37.8],
            'dst_lon': [-73.8],
            'dst_lat': [40.6]
        })

        fig = (
            ggplot(flights_df, aes(x='src_lon', y='src_lat', xend='dst_lon', yend='dst_lat'))
            + geom_map(map_type='usa')
            + geom_point(data=airports_df, mapping=aes(x='lon', y='lat'))
            + geom_edgebundle(
                C=2, I=5, verbose=False,
                show_highlight=True,
                highlight_color='yellow',
                highlight_alpha=0.6
            )
            + theme_dark()
        ).draw()

        # Should have point + edge + highlight traces
        geo_traces = [t for t in fig.data if t.type == 'scattergeo']
        assert len(geo_traces) >= 3  # 1 point + 1 edge + 1 highlight


class TestStatEdgebundleAdvanced:
    """Advanced tests for stat_edgebundle."""

    def test_large_network(self):
        """Test bundling on a larger network."""
        np.random.seed(123)
        n_edges = 50

        edges_df = pd.DataFrame({
            'x': np.random.uniform(0, 100, n_edges),
            'y': np.random.uniform(0, 100, n_edges),
            'xend': np.random.uniform(0, 100, n_edges),
            'yend': np.random.uniform(0, 100, n_edges)
        })

        stat = stat_edgebundle(C=3, I=20, verbose=False)
        bundled = stat.compute(edges_df)

        # Should have output for all edges
        assert bundled['group'].nunique() == n_edges

    def test_very_short_edges(self):
        """Test handling of very short edges."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 0],
            'xend': [0.001, 0.001],
            'yend': [0.001, 0.001]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)
        bundled = stat.compute(edges_df)

        # Should handle without errors
        assert len(bundled) > 0

    def test_overlapping_edges(self):
        """Test handling of exactly overlapping edges."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 0],
            'xend': [10, 10],
            'yend': [10, 10]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)
        bundled = stat.compute(edges_df)

        # Both edges should be bundled identically
        assert bundled['group'].nunique() == 2

    def test_parameter_ranges(self):
        """Test various parameter combinations."""
        edges_df = pd.DataFrame({
            'x': [0, 5],
            'y': [0, 5],
            'xend': [10, 15],
            'yend': [10, 15]
        })

        # Test extreme K values
        stat_low_k = stat_edgebundle(K=0.1, C=2, I=5, verbose=False)
        stat_high_k = stat_edgebundle(K=5.0, C=2, I=5, verbose=False)

        bundled_low_k = stat_low_k.compute(edges_df)
        bundled_high_k = stat_high_k.compute(edges_df)

        assert len(bundled_low_k) > 0
        assert len(bundled_high_k) > 0

    def test_step_size_effect(self):
        """Test that step size affects bundling."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        # Small step size
        stat_small_s = stat_edgebundle(S=0.01, C=2, I=10, verbose=False)
        bundled_small_s = stat_small_s.compute(edges_df)

        # Large step size
        stat_large_s = stat_edgebundle(S=0.1, C=2, I=10, verbose=False)
        bundled_large_s = stat_large_s.compute(edges_df)

        # Both should produce valid output
        assert len(bundled_small_s) > 0
        assert len(bundled_large_s) > 0


class TestColorConversion:
    """Tests for color conversion in geom_edgebundle."""

    def test_named_colors(self):
        """Test that named colors are converted correctly."""
        edges_df = pd.DataFrame({
            'x': [0],
            'y': [0],
            'xend': [10],
            'yend': [10]
        })

        named_colors = ['steelblue', 'red', 'green', 'orange', 'purple', 'magenta']

        for color in named_colors:
            fig = (
                ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
                + geom_edgebundle(C=1, I=2, verbose=False, color=color, show_highlight=False)
            ).draw()

            # Should not crash and should have traces
            assert len(fig.data) > 0
            # Color should be rgba format
            assert 'rgba' in fig.data[0].line.color

    def test_hex_colors(self):
        """Test that hex colors are converted correctly."""
        edges_df = pd.DataFrame({
            'x': [0],
            'y': [0],
            'xend': [10],
            'yend': [10]
        })

        # Test 6-digit hex
        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=1, I=2, verbose=False, color='#ff5500', alpha=0.7, show_highlight=False)
        ).draw()

        assert 'rgba(255,85,0,0.7)' in fig.data[0].line.color

    def test_rgba_passthrough(self):
        """Test that rgba colors pass through unchanged."""
        edges_df = pd.DataFrame({
            'x': [0],
            'y': [0],
            'xend': [10],
            'yend': [10]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=1, I=2, verbose=False, color='rgba(100,150,200,0.5)', show_highlight=False)
        ).draw()

        # Should pass through unchanged
        assert fig.data[0].line.color == 'rgba(100,150,200,0.5)'


class TestEdgeCases:
    """Edge case tests."""

    def test_nan_values_in_data(self):
        """Test handling of NaN values in edge data."""
        edges_df = pd.DataFrame({
            'x': [0, np.nan, 5],
            'y': [0, 2, 5],
            'xend': [10, 12, 15],
            'yend': [10, 12, 15]
        })

        # Drop NaN rows before processing
        edges_clean = edges_df.dropna()

        stat = stat_edgebundle(C=2, I=5, verbose=False)
        bundled = stat.compute(edges_clean)

        assert len(bundled) > 0
        assert bundled['group'].nunique() == 2

    def test_zero_length_edge(self):
        """Test handling of zero-length edge."""
        import warnings

        edges_df = pd.DataFrame({
            'x': [5],
            'y': [5],
            'xend': [5],
            'yend': [5]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            bundled = stat.compute(edges_df)

        # Should not crash
        assert len(bundled) > 0

    def test_negative_coordinates(self):
        """Test handling of negative coordinates."""
        edges_df = pd.DataFrame({
            'x': [-10, -5],
            'y': [-10, -5],
            'xend': [10, 15],
            'yend': [10, 15]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)
        bundled = stat.compute(edges_df)

        assert len(bundled) > 0

        # Check endpoints preserved
        edge0 = bundled[bundled['group'] == 0]
        assert abs(edge0.iloc[0]['x'] - (-10)) < 1e-5
        assert abs(edge0.iloc[0]['y'] - (-10)) < 1e-5


class TestIgraphSupport:
    """Tests for igraph Graph object support."""

    def test_igraph_basic(self):
        """Test basic igraph support."""
        pytest.importorskip("igraph")
        import igraph as ig

        # Create simple graph
        g = ig.Graph([(0, 1), (1, 2), (0, 2)])
        g.vs['x'] = [0, 5, 10]
        g.vs['y'] = [0, 5, 0]

        bundle = geom_edgebundle(graph=g, verbose=False, C=2, I=5)

        # Check that data was extracted
        assert bundle.data is not None
        assert len(bundle.data) == 3  # 3 edges
        assert 'x' in bundle.data.columns
        assert 'xend' in bundle.data.columns

        # Check that nodes were extracted
        assert bundle.nodes is not None
        assert len(bundle.nodes) == 3  # 3 nodes

    def test_igraph_with_lon_lat(self):
        """Test igraph with longitude/latitude attributes."""
        pytest.importorskip("igraph")
        import igraph as ig

        g = ig.Graph([(0, 1), (1, 2)])
        g.vs['longitude'] = [-100, -90, -80]
        g.vs['latitude'] = [40, 45, 40]
        g.vs['name'] = ['A', 'B', 'C']

        bundle = geom_edgebundle(graph=g, verbose=False, C=2, I=5)

        assert bundle.data is not None
        assert bundle.nodes is not None
        assert 'name' in bundle.nodes.columns

    def test_igraph_us_flights(self):
        """Test with us_flights dataset."""
        pytest.importorskip("igraph")
        from ggplotly import data

        g = data('us_flights')

        bundle = geom_edgebundle(graph=g, verbose=False, C=2, I=5)

        assert bundle.data is not None
        assert bundle.nodes is not None
        assert len(bundle.nodes) == 276
        assert 'name' in bundle.nodes.columns

    def test_igraph_node_params(self):
        """Test node visualization parameters."""
        pytest.importorskip("igraph")
        import igraph as ig

        g = ig.Graph([(0, 1)])
        g.vs['x'] = [0, 10]
        g.vs['y'] = [0, 10]

        bundle = geom_edgebundle(
            graph=g,
            verbose=False,
            show_nodes=True,
            node_color='red',
            node_size=5,
            node_alpha=0.5
        )

        assert bundle.params['show_nodes'] is True
        assert bundle.params['node_color'] == 'red'
        assert bundle.params['node_size'] == 5
        assert bundle.params['node_alpha'] == 0.5

    def test_igraph_draw(self):
        """Test that igraph geom draws correctly."""
        pytest.importorskip("igraph")
        import igraph as ig

        g = ig.Graph([(0, 1), (1, 2)])
        g.vs['x'] = [0, 5, 10]
        g.vs['y'] = [0, 5, 0]

        # Create geom and extract data for ggplot
        bundle = geom_edgebundle(graph=g, verbose=False, C=2, I=5)
        p = ggplot(bundle.data, aes(x='x', y='y', xend='xend', yend='yend')) + bundle
        fig = p.draw()

        # Should have traces for edges and nodes
        assert len(fig.data) > 0


class TestEdgeWeights:
    """Tests for edge weight support in bundling."""

    def test_stat_edgebundle_with_weights(self):
        """Test that stat_edgebundle accepts and uses weights."""
        edges_df = pd.DataFrame({
            'x': [0, 0, 0],
            'y': [0, 1, 2],
            'xend': [10, 10, 10],
            'yend': [0, 1, 2]
        })
        weights = np.array([10.0, 1.0, 1.0])

        stat = stat_edgebundle(C=2, I=10, verbose=False)
        bundled = stat.compute(edges_df, weights=weights)

        assert len(bundled) > 0
        assert 'x' in bundled.columns
        assert 'y' in bundled.columns

    def test_stat_edgebundle_weight_normalization(self):
        """Test that weights are normalized to [0.5, 1.5] range."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        # Test with extreme weight values
        weights = np.array([1.0, 1000.0])

        stat = stat_edgebundle(C=2, I=5, verbose=False)
        # Should not crash with extreme values
        bundled = stat.compute(edges_df, weights=weights)
        assert len(bundled) > 0

    def test_stat_edgebundle_uniform_weights(self):
        """Test that uniform weights behave like no weights."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        stat = stat_edgebundle(C=2, I=10, verbose=False)

        # Compute without weights
        bundled_no_weights = stat.compute(edges_df)

        # Clear cache
        stat._cached_result = None
        stat._cached_data_hash = None

        # Compute with uniform weights (should be same as no weights)
        uniform_weights = np.array([5.0, 5.0])
        bundled_uniform = stat.compute(edges_df, weights=uniform_weights)

        # Results should be identical (uniform weights normalize to 1.0)
        np.testing.assert_array_almost_equal(
            bundled_no_weights['x'].values,
            bundled_uniform['x'].values
        )

    def test_stat_edgebundle_weight_length_mismatch(self):
        """Test that mismatched weight length raises error."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })
        weights = np.array([1.0, 2.0, 3.0])  # Wrong length

        stat = stat_edgebundle(C=2, I=5, verbose=False)

        with pytest.raises(ValueError, match="weights length"):
            stat.compute(edges_df, weights=weights)

    def test_geom_edgebundle_with_weight_mapping(self):
        """Test geom_edgebundle with weight aesthetic mapping."""
        edges_df = pd.DataFrame({
            'x': [0, 0, 0],
            'y': [0, 1, 2],
            'xend': [10, 10, 10],
            'yend': [0, 1, 2],
            'traffic': [100, 10, 10]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', weight='traffic'))
            + geom_edgebundle(C=2, I=5, verbose=False, show_highlight=False)
        ).draw()

        assert len(fig.data) > 0

    def test_geom_edgebundle_with_weight_param(self):
        """Test geom_edgebundle with weight parameter."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1],
            'passengers': [500, 50]
        })

        bundle = geom_edgebundle(
            data=edges_df,
            weight='passengers',
            C=2, I=5,
            verbose=False
        )

        assert bundle.weight_attr == 'passengers'

    def test_geom_edgebundle_auto_detect_weight_column(self):
        """Test that geom_edgebundle auto-detects 'weight' column."""
        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1],
            'weight': [10.0, 1.0]
        })

        fig = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=2, I=5, verbose=False, show_highlight=False)
        ).draw()

        assert len(fig.data) > 0

    def test_igraph_with_edge_weights(self):
        """Test igraph support with edge weights."""
        pytest.importorskip("igraph")
        import igraph as ig

        g = ig.Graph([(0, 1), (1, 2), (0, 2)])
        g.vs['x'] = [0, 5, 10]
        g.vs['y'] = [0, 5, 0]
        g.es['weight'] = [100, 10, 10]  # First edge is heavy

        bundle = geom_edgebundle(graph=g, verbose=False, C=2, I=5)

        # Check that weight was extracted
        assert 'weight' in bundle.data.columns
        assert bundle.data['weight'].tolist() == [100, 10, 10]

    def test_igraph_with_custom_weight_attr(self):
        """Test igraph with custom weight attribute name."""
        pytest.importorskip("igraph")
        import igraph as ig

        g = ig.Graph([(0, 1), (1, 2)])
        g.vs['x'] = [0, 5, 10]
        g.vs['y'] = [0, 5, 0]
        g.es['passengers'] = [500, 50]

        bundle = geom_edgebundle(graph=g, weight='passengers', verbose=False, C=2, I=5)

        assert 'weight' in bundle.data.columns
        assert bundle.data['weight'].tolist() == [500, 50]

    def test_weights_affect_bundling(self):
        """Test that weights actually affect the bundling result."""
        # Create parallel edges where middle edge should bundle differently
        # based on whether it has high or low weight
        edges_df = pd.DataFrame({
            'x': [0, 0, 0],
            'y': [0, 0.5, 1],
            'xend': [10, 10, 10],
            'yend': [0, 0.5, 1]
        })

        stat = stat_edgebundle(C=3, I=20, verbose=False)

        # Heavy top edge - middle should bundle toward top
        stat._cached_result = None
        stat._cached_data_hash = None
        weights_top_heavy = np.array([100.0, 1.0, 1.0])
        bundled_top = stat.compute(edges_df, weights=weights_top_heavy)

        # Heavy bottom edge - middle should bundle toward bottom
        stat._cached_result = None
        stat._cached_data_hash = None
        weights_bottom_heavy = np.array([1.0, 1.0, 100.0])
        bundled_bottom = stat.compute(edges_df, weights=weights_bottom_heavy)

        # Middle edge (group 1) should have different y values
        middle_top = bundled_top[bundled_top['group'] == 1]
        middle_bottom = bundled_bottom[bundled_bottom['group'] == 1]

        # The bundled paths should be different
        assert not np.allclose(
            middle_top['y'].values,
            middle_bottom['y'].values,
            atol=0.01
        )

    def test_weights_pull_middle_edge_toward_heavy_group(self):
        """
        Test that heavy edges attract lighter edges more strongly.

        Creates 3 groups of parallel edges (top at y=8, middle at y=5, bottom at y=2).
        When top edges are heavy, middle should be pulled UP toward y=8.
        When bottom edges are heavy, middle should be pulled DOWN toward y=2.
        """
        edges_df = pd.DataFrame({
            # 3 top edges at y=8, 1 middle at y=5, 3 bottom at y=2
            'x':    [0, 0, 0,   0,   0, 0, 0],
            'y':    [8, 8, 8,   5,   2, 2, 2],
            'xend': [10, 10, 10, 10,  10, 10, 10],
            'yend': [8, 8, 8,   5,   2, 2, 2],
        })

        stat = stat_edgebundle(C=4, I=30, compatibility_threshold=0.5, verbose=False)

        # No weights - middle should stay centered
        bundled_none = stat.compute(edges_df, weights=None)

        stat._cached_result = None
        stat._cached_data_hash = None

        # Heavy top - middle should be pulled UP
        weights_heavy_top = np.array([100, 100, 100,  1,  1, 1, 1])
        bundled_top = stat.compute(edges_df, weights=weights_heavy_top)

        stat._cached_result = None
        stat._cached_data_hash = None

        # Heavy bottom - middle should be pulled DOWN
        weights_heavy_bottom = np.array([1, 1, 1,  1,  100, 100, 100])
        bundled_bottom = stat.compute(edges_df, weights=weights_heavy_bottom)

        # Get midpoint y-values for the middle edge (group 3)
        def get_midpoint_y(bundled):
            group = bundled[bundled['group'] == 3]
            mid_idx = len(group) // 2
            return group.iloc[mid_idx]['y']

        mid_y_none = get_midpoint_y(bundled_none)
        mid_y_top = get_midpoint_y(bundled_top)
        mid_y_bottom = get_midpoint_y(bundled_bottom)

        # With no weights, middle should stay at y=5 (centered)
        assert abs(mid_y_none - 5.0) < 0.1, f"Unweighted middle should stay near y=5, got {mid_y_none}"

        # With heavy top, middle should be pulled UP (y > 5)
        assert mid_y_top > 5.5, f"Heavy top should pull middle UP above 5.5, got {mid_y_top}"

        # With heavy bottom, middle should be pulled DOWN (y < 5)
        assert mid_y_bottom < 4.5, f"Heavy bottom should pull middle DOWN below 4.5, got {mid_y_bottom}"

        # The difference between heavy-top and heavy-bottom should be significant
        assert mid_y_top - mid_y_bottom > 2.0, (
            f"Weight effect should create >2.0 difference, got {mid_y_top - mid_y_bottom:.2f}"
        )


class TestCaching:
    """Tests for caching functionality in stat_edgebundle and geom_edgebundle."""

    def test_stat_edgebundle_cache_hit(self):
        """Test that identical calls return cached result."""
        from ggplotly.stats.stat_edgebundle import _bundling_cache, clear_bundling_cache

        clear_bundling_cache()

        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)

        # First call - should compute and cache
        result1 = stat.compute(edges_df)
        cache_size_after_first = len(_bundling_cache)
        assert cache_size_after_first == 1

        # Second call with same data - should use cache
        result2 = stat.compute(edges_df)
        cache_size_after_second = len(_bundling_cache)
        assert cache_size_after_second == 1  # No new cache entry

        # Results should be identical
        pd.testing.assert_frame_equal(result1, result2)

    def test_stat_edgebundle_cache_miss_different_data(self):
        """Test that different data creates new cache entry."""
        from ggplotly.stats.stat_edgebundle import _bundling_cache, clear_bundling_cache

        clear_bundling_cache()

        edges_df1 = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        edges_df2 = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 2],  # Different y value
            'xend': [10, 10],
            'yend': [0, 2]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)

        stat.compute(edges_df1)
        assert len(_bundling_cache) == 1

        stat.compute(edges_df2)
        assert len(_bundling_cache) == 2  # New cache entry

    def test_stat_edgebundle_cache_miss_different_params(self):
        """Test that different algorithm parameters create new cache entry."""
        from ggplotly.stats.stat_edgebundle import _bundling_cache, clear_bundling_cache

        clear_bundling_cache()

        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        stat1 = stat_edgebundle(C=2, I=5, verbose=False)
        stat2 = stat_edgebundle(C=3, I=5, verbose=False)  # Different C

        stat1.compute(edges_df)
        assert len(_bundling_cache) == 1

        stat2.compute(edges_df)
        assert len(_bundling_cache) == 2  # New cache entry due to different params

    def test_stat_edgebundle_cache_miss_different_weights(self):
        """Test that different weights create new cache entry."""
        from ggplotly.stats.stat_edgebundle import _bundling_cache, clear_bundling_cache

        clear_bundling_cache()

        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)

        weights1 = np.array([1.0, 1.0])
        weights2 = np.array([10.0, 1.0])  # Different weights

        stat.compute(edges_df, weights=weights1)
        assert len(_bundling_cache) == 1

        stat.compute(edges_df, weights=weights2)
        assert len(_bundling_cache) == 2  # New cache entry

    def test_stat_edgebundle_cache_hit_with_weights(self):
        """Test cache hit when same weights are used."""
        from ggplotly.stats.stat_edgebundle import _bundling_cache, clear_bundling_cache

        clear_bundling_cache()

        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)
        weights = np.array([5.0, 10.0])

        result1 = stat.compute(edges_df, weights=weights)
        assert len(_bundling_cache) == 1

        result2 = stat.compute(edges_df, weights=weights.copy())  # Same values
        assert len(_bundling_cache) == 1  # Cache hit

        pd.testing.assert_frame_equal(result1, result2)

    def test_clear_bundling_cache(self):
        """Test that clear_bundling_cache clears the cache."""
        from ggplotly.stats.stat_edgebundle import _bundling_cache, clear_bundling_cache

        clear_bundling_cache()

        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        stat = stat_edgebundle(C=2, I=5, verbose=False)
        stat.compute(edges_df)
        assert len(_bundling_cache) >= 1

        clear_bundling_cache()
        assert len(_bundling_cache) == 0

    def test_cache_survives_stat_deepcopy(self):
        """Test that cache persists across deepcopy of stat objects."""
        import copy

        from ggplotly.stats.stat_edgebundle import _bundling_cache, clear_bundling_cache

        clear_bundling_cache()

        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        stat1 = stat_edgebundle(C=2, I=5, verbose=False)
        result1 = stat1.compute(edges_df)
        assert len(_bundling_cache) == 1

        # Deep copy the stat (this happens during ggplot processing)
        stat2 = copy.deepcopy(stat1)

        # Compute with the copy - should hit cache
        result2 = stat2.compute(edges_df)
        assert len(_bundling_cache) == 1  # Still just one entry

        pd.testing.assert_frame_equal(result1, result2)

    def test_geom_edgebundle_uses_cache(self):
        """Test that geom_edgebundle uses the stat cache correctly."""
        from ggplotly.stats.stat_edgebundle import _bundling_cache, clear_bundling_cache

        clear_bundling_cache()

        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        # First plot - should populate cache
        fig1 = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=2, I=5, verbose=False, show_highlight=False)
        ).draw()
        cache_size_after_first = len(_bundling_cache)
        assert cache_size_after_first >= 1

        # Second plot with same data and params - should use cache
        fig2 = (
            ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
            + geom_edgebundle(C=2, I=5, verbose=False, show_highlight=False)
        ).draw()
        cache_size_after_second = len(_bundling_cache)
        assert cache_size_after_second == cache_size_after_first

    def test_cache_key_includes_all_params(self):
        """Test that cache key includes all relevant algorithm parameters."""
        from ggplotly.stats.stat_edgebundle import _bundling_cache, clear_bundling_cache

        clear_bundling_cache()

        edges_df = pd.DataFrame({
            'x': [0, 0],
            'y': [0, 1],
            'xend': [10, 10],
            'yend': [0, 1]
        })

        # Create stats with different parameter variations
        param_variations = [
            {'K': 1.0, 'E': 1.0, 'C': 2, 'P': 1, 'S': 0.04, 'P_rate': 2, 'I': 5, 'I_rate': 2/3, 'compatibility_threshold': 0.6},
            {'K': 2.0, 'E': 1.0, 'C': 2, 'P': 1, 'S': 0.04, 'P_rate': 2, 'I': 5, 'I_rate': 2/3, 'compatibility_threshold': 0.6},  # Different K
            {'K': 1.0, 'E': 2.0, 'C': 2, 'P': 1, 'S': 0.04, 'P_rate': 2, 'I': 5, 'I_rate': 2/3, 'compatibility_threshold': 0.6},  # Different E
            {'K': 1.0, 'E': 1.0, 'C': 2, 'P': 2, 'S': 0.04, 'P_rate': 2, 'I': 5, 'I_rate': 2/3, 'compatibility_threshold': 0.6},  # Different P
            {'K': 1.0, 'E': 1.0, 'C': 2, 'P': 1, 'S': 0.08, 'P_rate': 2, 'I': 5, 'I_rate': 2/3, 'compatibility_threshold': 0.6},  # Different S
            {'K': 1.0, 'E': 1.0, 'C': 2, 'P': 1, 'S': 0.04, 'P_rate': 3, 'I': 5, 'I_rate': 2/3, 'compatibility_threshold': 0.6},  # Different P_rate
            {'K': 1.0, 'E': 1.0, 'C': 2, 'P': 1, 'S': 0.04, 'P_rate': 2, 'I': 10, 'I_rate': 2/3, 'compatibility_threshold': 0.6}, # Different I
            {'K': 1.0, 'E': 1.0, 'C': 2, 'P': 1, 'S': 0.04, 'P_rate': 2, 'I': 5, 'I_rate': 0.5, 'compatibility_threshold': 0.6},  # Different I_rate
            {'K': 1.0, 'E': 1.0, 'C': 2, 'P': 1, 'S': 0.04, 'P_rate': 2, 'I': 5, 'I_rate': 2/3, 'compatibility_threshold': 0.8},  # Different threshold
        ]

        for params in param_variations:
            stat = stat_edgebundle(verbose=False, **params)
            stat.compute(edges_df)

        # Each parameter variation should create a unique cache entry
        assert len(_bundling_cache) == len(param_variations)
