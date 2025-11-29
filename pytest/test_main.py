import sys
import os

import pandas as pd
import plotly.graph_objects as go
import numpy as np

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import *


def test_basic_plot():
    # Sample Data
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

    # Create a plot with coord_flip
    p = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_flip()
    plotly_fig = p.draw()

    # Assert that the returned object is a Plotly figure
    assert isinstance(plotly_fig, go.Figure), "The plot is not a Plotly figure"


def test_basic_plot_with_labels_and_theme():
    # Sample Data
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

    # Create a plot with additional labels and theme
    p = (
        ggplot(df, aes(x="x", y="y"))
        + geom_point()
        + labs(
            title="Main Title",
            subtitle="This is a subtitle",
            x="X-Axis",
            y="Y-Axis",
            caption="Data source: XYZ",
        )
        + theme_minimal()
    )
    plotly_fig = p.draw()

    # Assert that the returned object is a Plotly figure
    assert isinstance(plotly_fig, go.Figure), "The plot is not a Plotly figure"
    assert (
        "Main Title" in plotly_fig.layout.title.text and 
        "This is a subtitle" in plotly_fig.layout.title.text
    )
    assert (
        plotly_fig.layout.xaxis.title.text == "X-Axis"
    )
    assert (
        plotly_fig.layout.yaxis.title.text == "Y-Axis"
    )
    assert (
        plotly_fig.layout.annotations[0].text == "Data source: XYZ"
    )


def test_basic_plot_with_ggtitle():
    # Sample Data
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

    # Create Plot with Title
    p = (
        ggplot(df, aes(x="x", y="y"))
        + geom_point()
        + ggtitle("My Plot Title")
        + theme_minimal()
    )
    plotly_fig = p.draw()

    # Assert that the returned object is a Plotly figure
    assert isinstance(plotly_fig, go.Figure), "The plot is not a Plotly figure"
    assert (
        "My Plot Title" in plotly_fig.layout.title.text
    )


def test_all_geoms():
    for func in [geom_point, geom_line, geom_bar, geom_histogram, geom_area]:
        # Sample Data
        df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

        # Create Plot with Geom Function
        p = (
            ggplot(df, aes(x="x", y="y"))
            + func()
            + theme_minimal()
        )
        plotly_fig = p.draw()

        # Assert that the returned object is a Plotly figure
        assert isinstance(plotly_fig, go.Figure), f"The plot with {func.__name__} is not a Plotly figure"


# def test_area_plot_with_faceting():
#     # Sample Data
#     df = pd.DataFrame(
#         {
#             "x": np.linspace(0, 10, 100),
#             "y": np.sin(np.linspace(0, 10, 100)),
#             "category": np.random.choice(["A", "B"], 100),
#         }
#     )

#     # Area Plot with Faceting
#     p = (
#         ggplot(df, aes(x="x", y="y"))
#         + geom_area(fill="lightblue", alpha=0.5)
#         + facet_wrap("category")
#         + theme_minimal()
#     )
#     plotly_fig = p.draw()

#     # Assert that the returned object is a Plotly figure
#     assert isinstance(plotly_fig, go.Figure), "The plot is not a Plotly figure"


def test_shape_aesthetic_mapped_to_column():
    """Test shape aesthetic mapped to a categorical column."""
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6],
        'y': [1, 2, 3, 4, 5, 6],
        'species': ['A', 'A', 'B', 'B', 'C', 'C']
    })

    p = ggplot(df, aes(x='x', y='y', shape='species')) + geom_point(size=10)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 3, "Should have 3 traces (one per species)"

    # Check that each trace has a different symbol
    symbols = [trace.marker.symbol for trace in fig.data]
    assert len(set(symbols)) == 3, "Each species should have a different shape"
    assert 'circle' in symbols, "First shape should be circle"


def test_shape_aesthetic_literal_value():
    """Test shape aesthetic with a literal Plotly symbol."""
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})

    p = ggplot(df, aes(x='x', y='y')) + geom_point(shape='diamond', size=10)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 1, "Should have 1 trace"
    assert fig.data[0].marker.symbol == 'diamond', "Shape should be diamond"


def test_shape_and_color_both_mapped():
    """Test when both shape and color are mapped to columns."""
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6, 7, 8],
        'y': [1, 2, 3, 4, 5, 6, 7, 8],
        'color_var': ['Red', 'Red', 'Blue', 'Blue', 'Red', 'Red', 'Blue', 'Blue'],
        'shape_var': ['Circle', 'Square', 'Circle', 'Square', 'Circle', 'Square', 'Circle', 'Square']
    })

    p = ggplot(df, aes(x='x', y='y', color='color_var', shape='shape_var')) + geom_point(size=10)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # Should create traces for each combination: Red+Circle, Red+Square, Blue+Circle, Blue+Square
    assert len(fig.data) == 4, "Should have 4 traces (2 colors x 2 shapes)"

    # Check that we have different colors and shapes
    colors = set(trace.marker.color for trace in fig.data)
    symbols = set(trace.marker.symbol for trace in fig.data)
    assert len(colors) == 2, "Should have 2 different colors"
    assert len(symbols) == 2, "Should have 2 different shapes"


def test_shape_and_color_same_column():
    """Test when both shape and color are mapped to the same column."""
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6],
        'y': [1, 2, 3, 4, 5, 6],
        'species': ['A', 'A', 'B', 'B', 'C', 'C']
    })

    p = ggplot(df, aes(x='x', y='y', color='species', shape='species')) + geom_point(size=10)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # When same column is used for both aesthetics, should have 3 traces (one per species)
    assert len(fig.data) == 3, "Should have 3 traces"

    # Check that colors and shapes are both varied
    colors = set(trace.marker.color for trace in fig.data)
    symbols = set(trace.marker.symbol for trace in fig.data)
    assert len(colors) == 3, "Should have 3 different colors"
    assert len(symbols) == 3, "Should have 3 different shapes"

    # Check that trace names are simple (not "A, A" but just "A")
    trace_names = [trace.name for trace in fig.data]
    assert 'A' in trace_names and 'B' in trace_names and 'C' in trace_names, \
        "Trace names should be simple category names when color and shape use same column"


def test_scale_shape_manual():
    """Test scale_shape_manual for custom shape mappings."""
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6],
        'y': [1, 2, 3, 4, 5, 6],
        'species': ['A', 'A', 'B', 'B', 'C', 'C']
    })

    p = (ggplot(df, aes(x='x', y='y', shape='species'))
         + geom_point(size=10)
         + scale_shape_manual(values={'A': 'star', 'B': 'hexagon', 'C': 'cross'}))
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 3, "Should have 3 traces"

    # Check custom shapes were applied
    shape_map = {trace.name: trace.marker.symbol for trace in fig.data}
    assert shape_map['A'] == 'star', "Species A should have star shape"
    assert shape_map['B'] == 'hexagon', "Species B should have hexagon shape"
    assert shape_map['C'] == 'cross', "Species C should have cross shape"


def test_geom_jitter_basic():
    """Test basic geom_jitter functionality with categorical x."""
    np.random.seed(42)
    df = pd.DataFrame({
        'category': ['A', 'A', 'A', 'B', 'B', 'B'],
        'value': [1, 2, 3, 4, 5, 6]
    })

    p = ggplot(df, aes(x='category', y='value')) + geom_jitter(width=0.2)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 1, "Should have 1 trace"
    # For categorical x, uses go.Box with boxpoints='all' for proper jitter
    assert fig.data[0].boxpoints == 'all', "Should use boxpoints='all' for jitter"
    assert fig.data[0].jitter > 0, "Should have jitter set"


def test_geom_jitter_categorical_x_uses_box():
    """Test that categorical x uses go.Box for proper alignment with boxplot."""
    np.random.seed(42)
    df = pd.DataFrame({
        'category': np.repeat(['A', 'B', 'C'], 20),
        'value': np.random.normal(10, 2, 60)
    })

    p = ggplot(df, aes(x='category', y='value')) + geom_jitter(width=0.2, seed=42)
    fig = p.draw()

    # Categorical x should use Box trace type for proper alignment
    assert fig.data[0].type == 'box', "Categorical x should use Box trace"
    # Box should be invisible (only points visible)
    assert fig.data[0].line.color == 'rgba(0,0,0,0)', "Box outline should be invisible"


def test_geom_jitter_with_color():
    """Test geom_jitter with color aesthetic."""
    np.random.seed(42)
    df = pd.DataFrame({
        'category': np.repeat(['A', 'B'], 10),
        'value': np.random.normal(10, 2, 20),
        'group': np.tile(['X', 'Y'], 10)
    })

    p = ggplot(df, aes(x='category', y='value', color='group')) + geom_jitter(width=0.2)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 2, "Should have 2 traces (one per color group)"

    # Check that colors are different
    colors = set(trace.marker.color for trace in fig.data)
    assert len(colors) == 2, "Should have 2 different colors"


def test_geom_jitter_seed_reproducibility():
    """Test that seed parameter produces reproducible jitter with numeric data."""
    df = pd.DataFrame({
        'x': [1, 1, 1, 2, 2, 2],
        'y': [1, 2, 3, 4, 5, 6]
    })

    p1 = ggplot(df, aes(x='x', y='y')) + geom_jitter(width=0.2, seed=123)
    fig1 = p1.draw()

    p2 = ggplot(df, aes(x='x', y='y')) + geom_jitter(width=0.2, seed=123)
    fig2 = p2.draw()

    # Same seed should produce same x positions for numeric data
    assert list(fig1.data[0].x) == list(fig2.data[0].x), "Same seed should produce same jitter"


def test_geom_jitter_width_parameter():
    """Test that width parameter controls jitter amount with numeric data."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.ones(100),
        'y': np.ones(100)
    })

    # Small width
    p_small = ggplot(df, aes(x='x', y='y')) + geom_jitter(width=0.1, seed=42)
    fig_small = p_small.draw()

    # Large width
    p_large = ggplot(df, aes(x='x', y='y')) + geom_jitter(width=0.4, seed=42)
    fig_large = p_large.draw()

    # Calculate spread for numeric data
    x_small = np.array(fig_small.data[0].x)
    x_large = np.array(fig_large.data[0].x)

    spread_small = x_small.max() - x_small.min()
    spread_large = x_large.max() - x_large.min()

    assert spread_large > spread_small, "Larger width should produce larger spread"


def test_geom_jitter_numeric_x():
    """Test geom_jitter with numeric x values."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'y': [1, 2, 3, 4, 5, 6, 7, 8, 9]
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_jitter(width=0.2, seed=42)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # X values should be jittered around 1, 2, 3
    x_values = fig.data[0].x
    assert len(set(x_values)) == 9, "All x values should be unique after jittering"


def test_geom_rug_basic():
    """Test basic geom_rug functionality."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 50),
        'y': np.random.normal(0, 1, 50)
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_point() + geom_rug()
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # Should have point trace + 2 rug traces (bottom and left by default)
    assert len(fig.data) >= 3, "Should have at least 3 traces (points + 2 rugs)"


def test_geom_rug_bottom_only():
    """Test geom_rug with only bottom side."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 20),
        'y': np.random.normal(0, 1, 20)
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_point() + geom_rug(sides='b')
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # Should have point trace + 1 rug trace (bottom only)
    assert len(fig.data) == 2, "Should have 2 traces (points + bottom rug)"


def test_geom_rug_all_sides():
    """Test geom_rug with all four sides."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 20),
        'y': np.random.normal(0, 1, 20)
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_point() + geom_rug(sides='bltr')
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # Should have point trace + 4 rug traces
    assert len(fig.data) == 5, "Should have 5 traces (points + 4 rugs)"


def test_geom_rug_custom_color():
    """Test geom_rug with custom color."""
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [1, 2, 3, 4, 5]
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_rug(color='red', sides='b')
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # Check that rug has red color
    assert fig.data[0].line.color == 'red', "Rug color should be red"


def test_geom_rug_length_parameter():
    """Test that length parameter affects rug tick length."""
    df = pd.DataFrame({
        'x': [0, 10],
        'y': [0, 10]
    })

    # Create rug with specific length
    p = ggplot(df, aes(x='x', y='y')) + geom_rug(sides='b', length=0.1)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # Check that y values of rug extend from min y
    y_coords = [y for y in fig.data[0].y if y is not None]
    # Rug should extend from 0 to 1 (10% of range 0-10)
    assert max(y_coords) == 1.0, f"Rug should extend 10% of y range, got {max(y_coords)}"


def test_geom_abline_basic():
    """Test basic geom_abline functionality."""
    df = pd.DataFrame({
        'x': [0, 1, 2, 3, 4],
        'y': [0, 1, 2, 3, 4]
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_point() + geom_abline(slope=1, intercept=0)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # Should have point trace + abline trace
    assert len(fig.data) == 2, "Should have 2 traces (points + abline)"
    assert fig.data[1].mode == 'lines', "abline should be a line"


def test_geom_abline_custom_slope_intercept():
    """Test geom_abline with custom slope and intercept."""
    df = pd.DataFrame({
        'x': [0, 1, 2, 3, 4],
        'y': [0, 2, 4, 6, 8]
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_abline(slope=2, intercept=1)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # Check that the line has correct slope (y = 2x + 1)
    x_vals = fig.data[0].x
    y_vals = fig.data[0].y
    # At x=0, y should be 1; at x=1, y should be 3
    # The actual values will be at the extremes, so check the relationship
    slope = (y_vals[1] - y_vals[0]) / (x_vals[1] - x_vals[0])
    assert slope == 2, f"Slope should be 2, got {slope}"


def test_geom_abline_custom_color():
    """Test geom_abline with custom color."""
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 2, 3]})

    p = ggplot(df, aes(x='x', y='y')) + geom_abline(slope=1, intercept=0, color='red')
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert fig.data[0].line.color == 'red', "Line color should be red"


def test_geom_abline_linetype():
    """Test geom_abline with different line types."""
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 2, 3]})

    p = ggplot(df, aes(x='x', y='y')) + geom_abline(slope=1, intercept=0, linetype='dash')
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert fig.data[0].line.dash == 'dash', "Line type should be dash"


def test_geom_abline_multiple_lines():
    """Test geom_abline with multiple slopes and intercepts."""
    df = pd.DataFrame({'x': [1, 2, 3], 'y': [1, 2, 3]})

    p = ggplot(df, aes(x='x', y='y')) + geom_abline(slope=[1, 2], intercept=[0, -1])
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 2, "Should have 2 traces (2 lines)"


def test_geom_contour_basic():
    """Test basic geom_contour functionality with 2D KDE."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 100),
        'y': np.random.normal(0, 1, 100)
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_contour()
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 1, "Should have 1 trace (contour)"
    assert fig.data[0].type == 'contour', "Should be a contour trace"


def test_geom_contour_with_points():
    """Test geom_contour layered with points."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 50),
        'y': np.random.normal(0, 1, 50)
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_contour(bins=5) + geom_point(alpha=0.5)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 2, "Should have 2 traces (contour + points)"


def test_geom_contour_custom_bins():
    """Test geom_contour with custom number of bins."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 100),
        'y': np.random.normal(0, 1, 100)
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_contour(bins=20)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert fig.data[0].ncontours == 20, "Should have 20 contour levels"


def test_geom_contour_filled_basic():
    """Test basic geom_contour_filled functionality."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 100),
        'y': np.random.normal(0, 1, 100)
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_contour_filled()
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 1, "Should have 1 trace (filled contour)"
    assert fig.data[0].type == 'contour', "Should be a contour trace"


def test_geom_contour_filled_palette():
    """Test geom_contour_filled with custom palette."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 100),
        'y': np.random.normal(0, 1, 100)
    })

    p = ggplot(df, aes(x='x', y='y')) + geom_contour_filled(palette='Plasma')
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert fig.data[0].colorscale is not None, "Should have a palette/colorscale"


def test_geom_contour_filled_with_points():
    """Test geom_contour_filled layered with points."""
    np.random.seed(42)
    df = pd.DataFrame({
        'x': np.random.normal(0, 1, 50),
        'y': np.random.normal(0, 1, 50)
    })

    p = (ggplot(df, aes(x='x', y='y'))
         + geom_contour_filled(alpha=0.5, bins=8)
         + geom_point(color='white', size=5))
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 2, "Should have 2 traces (contour + points)"


# ==================== geom_map tests ====================

def test_geom_map_usa_basic():
    """Test basic US states choropleth map (ggplot2 style with map_id)."""
    df = pd.DataFrame({
        'state': ['CA', 'TX', 'NY', 'FL', 'IL'],
        'value': [100, 80, 90, 70, 60]
    })

    p = ggplot(df, aes(map_id='state', fill='value')) + geom_map()
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 1, "Should have 1 trace (choropleth)"
    assert fig.data[0].type == 'choropleth', "Should be a choropleth trace"


def test_geom_map_usa_custom_palette():
    """Test US map with custom palette."""
    df = pd.DataFrame({
        'state': ['CA', 'TX', 'NY', 'FL'],
        'population': [39, 29, 19, 21]
    })

    p = ggplot(df, aes(map_id='state', fill='population')) + geom_map(palette='Blues')
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert fig.data[0].colorscale is not None, "Should have a colorscale"


def test_geom_map_world():
    """Test world map with country codes."""
    df = pd.DataFrame({
        'country': ['USA', 'CAN', 'MEX', 'BRA', 'ARG'],
        'gdp': [21, 1.6, 1.2, 1.4, 0.4]
    })

    p = ggplot(df, aes(map_id='country', fill='gdp')) + geom_map(map_type='world')
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert fig.data[0].locationmode == 'ISO-3', "Should use ISO-3 location mode"


def test_geom_map_with_map_data():
    """Test map with map_data() function like ggplot2."""
    from ggplotly import map_data

    states = map_data('state')
    df = pd.DataFrame({
        'state': ['CA', 'TX', 'NY', 'FL', 'IL'],
        'value': [100, 80, 90, 70, 60]
    })

    p = ggplot(df, aes(map_id='state', fill='value')) + geom_map(map=states)
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 1, "Should have 1 trace"
    # With map data, should include all states from map_data
    assert len(fig.data[0].locations) == len(states), "Should have all states from map_data"


def test_geom_map_categorical_fill():
    """Test map with categorical fill values."""
    df = pd.DataFrame({
        'state': ['CA', 'TX', 'NY', 'FL', 'IL', 'PA'],
        'region': ['West', 'South', 'Northeast', 'South', 'Midwest', 'Northeast']
    })

    p = ggplot(df, aes(map_id='state', fill='region')) + geom_map()
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 1, "Should have 1 trace"


def test_geom_map_no_fill():
    """Test map without fill aesthetic."""
    df = pd.DataFrame({
        'state': ['CA', 'TX', 'NY', 'FL']
    })

    p = ggplot(df, aes(map_id='state')) + geom_map()
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert fig.data[0].showscale == False, "Should not show colorbar without fill"


# ==================== geom_point_map tests ====================

def test_geom_point_map_basic():
    """Test basic point map with x=lon, y=lat (ggplot2 style)."""
    df = pd.DataFrame({
        'city': ['New York', 'Los Angeles', 'Chicago'],
        'lat': [40.7128, 34.0522, 41.8781],
        'lon': [-74.0060, -118.2437, -87.6298]
    })

    p = ggplot(df, aes(x='lon', y='lat')) + geom_point_map()
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert len(fig.data) == 1, "Should have 1 trace (scatter geo)"
    assert fig.data[0].type == 'scattergeo', "Should be a scattergeo trace"


def test_geom_point_map_with_color():
    """Test point map with color mapping."""
    df = pd.DataFrame({
        'city': ['New York', 'Los Angeles', 'Chicago', 'Houston'],
        'lat': [40.7128, 34.0522, 41.8781, 29.7604],
        'lon': [-74.0060, -118.2437, -87.6298, -95.3698],
        'population': [8.3, 3.9, 2.7, 2.3]
    })

    p = ggplot(df, aes(x='lon', y='lat', color='population')) + geom_point_map()
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert fig.data[0].marker.colorscale is not None, "Should have a colorscale"


def test_geom_point_map_with_size():
    """Test point map with size mapping."""
    df = pd.DataFrame({
        'city': ['New York', 'Los Angeles', 'Chicago'],
        'lat': [40.7128, 34.0522, 41.8781],
        'lon': [-74.0060, -118.2437, -87.6298],
        'value': [100, 50, 75]
    })

    p = ggplot(df, aes(x='lon', y='lat', size='value')) + geom_point_map()
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    # Size should vary
    assert len(set(fig.data[0].marker.size)) > 1, "Point sizes should vary"


def test_geom_point_map_world():
    """Test point map on world map."""
    df = pd.DataFrame({
        'city': ['London', 'Tokyo', 'Sydney'],
        'lat': [51.5074, 35.6762, -33.8688],
        'lon': [-0.1278, 139.6503, 151.2093]
    })

    p = ggplot(df, aes(x='lon', y='lat')) + geom_point_map(map='world')
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert fig.layout.geo.scope == 'world', "Should have world scope"


def test_geom_point_map_with_labels():
    """Test point map with text labels."""
    df = pd.DataFrame({
        'city': ['NYC', 'LA', 'CHI'],
        'lat': [40.7128, 34.0522, 41.8781],
        'lon': [-74.0060, -118.2437, -87.6298]
    })

    p = ggplot(df, aes(x='lon', y='lat', label='city')) + geom_point_map()
    fig = p.draw()

    assert isinstance(fig, go.Figure), "The plot is not a Plotly figure"
    assert 'text' in fig.data[0].mode, "Should have text in mode"


# def test_plot_with_faceting_2():
#     # Sample Data
#     np.random.seed(0)
#     df = pd.DataFrame(
#         {
#             "x": np.random.randn(200),
#             "y": np.random.randn(200),
#             "category": np.random.choice(["A", "B"], size=200),
#         }
#     )

#     # Create Plot with Faceting
#     p = (
#         ggplot(df, aes(x="x", y="y"))
#         + geom_point(color="blue", alpha=0.5)
#         + geom_smooth(method="loess", color="red")
#         + facet_wrap("category", ncol=1)
#         + theme_minimal()
#     )
#     plotly_fig = p.draw()

#     # Assert that the returned object is a Plotly figure
#     assert isinstance(plotly_fig, go.Figure), "The plot is not a Plotly figure"
