import sys
import os

import pandas as pd
import plotly.graph_objects as go
import numpy as np

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import *


def test_first():
    # Sample Data
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

    # Create a plot with coord_flip
    p = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_flip()
    plotly_fig = p.draw()

    # Assert that the returned object is a Plotly figure
    assert isinstance(plotly_fig, go.Figure), "The plot is not a Plotly figure"


def test_2():
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


def test_3():
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


def test_4():
    # Sample Data
    df = pd.DataFrame({"x": [1, 2, 3], "y": [4, 5, 6]})

    # Create Plot with Title
    p = (
        ggplot(df, aes(x="x", y="y"))
        + geom_point()
        + labs(title="My Plot Title", x="X-Axis Label", y="Y-Axis Label")
        + theme_minimal()
    )
    plotly_fig = p.draw()

    # Assert that the returned object is a Plotly figure
    assert isinstance(plotly_fig, go.Figure), "The plot is not a Plotly figure"


def test_area_plot_with_faceting():
    # Sample Data
    df = pd.DataFrame(
        {
            "x": np.linspace(0, 10, 100),
            "y": np.sin(np.linspace(0, 10, 100)),
            "category": np.random.choice(["A", "B"], 100),
        }
    )

    # Area Plot with Faceting
    p = (
        ggplot(df, aes(x="x", y="y"))
        + geom_area(fill="lightblue", alpha=0.5)
        + facet_wrap("category")
        + theme_minimal()
    )
    plotly_fig = p.draw()

    # Assert that the returned object is a Plotly figure
    assert isinstance(plotly_fig, go.Figure), "The plot is not a Plotly figure"


def test_plot_with_faceting_2():
    # Sample Data
    np.random.seed(0)
    df = pd.DataFrame(
        {
            "x": np.random.randn(200),
            "y": np.random.randn(200),
            "category": np.random.choice(["A", "B"], size=200),
        }
    )

    # Create Plot with Faceting
    p = (
        ggplot(df, aes(x="x", y="y"))
        + geom_point(color="blue", alpha=0.5)
        + geom_smooth(method="loess", color="red")
        + facet_wrap("category", ncol=1)
        + theme_minimal()
    )
    plotly_fig = p.draw()

    # Assert that the returned object is a Plotly figure
    assert isinstance(plotly_fig, go.Figure), "The plot is not a Plotly figure"
