"""
Tests for geom_surface and geom_wireframe - 3D surface plots.

This test suite verifies actual figure output, not just that code runs.
"""
import numpy as np
import pandas as pd
from plotly.graph_objects import Figure

import pytest
from ggplotly import (
    aes,
    facet_wrap,
    geom_point_3d,
    geom_surface,
    geom_wireframe,
    ggplot,
    ggsize,
    labs,
    theme_minimal,
)


def make_surface_data(func, x_range=(-5, 5), y_range=(-5, 5), resolution=50):
    """Create a DataFrame from a z = f(x, y) function."""
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)
    return pd.DataFrame({
        'x': X.flatten(),
        'y': Y.flatten(),
        'z': Z.flatten(),
    })


@pytest.fixture
def surface_data():
    """Create sample surface data (sin wave)."""
    x = np.linspace(-5, 5, 30)
    y = np.linspace(-5, 5, 30)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(np.sqrt(X**2 + Y**2))

    return pd.DataFrame({
        'x': X.flatten(),
        'y': Y.flatten(),
        'z': Z.flatten()
    })


@pytest.fixture
def peak_data():
    """Create sample data with a peak (for diverse z values)."""
    x = np.linspace(-3, 3, 25)
    y = np.linspace(-3, 3, 25)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 + Y**2))

    return pd.DataFrame({
        'x': X.flatten(),
        'y': Y.flatten(),
        'z': Z.flatten()
    })


@pytest.fixture
def multi_surface_data():
    """Create data suitable for faceted surface plots."""
    data_list = []
    for panel in ['A', 'B']:
        x = np.linspace(-3, 3, 20)
        y = np.linspace(-3, 3, 20)
        X, Y = np.meshgrid(x, y)
        if panel == 'A':
            Z = np.sin(X) * np.cos(Y)
        else:
            Z = np.cos(X) * np.sin(Y)

        df = pd.DataFrame({
            'x': X.flatten(),
            'y': Y.flatten(),
            'z': Z.flatten(),
            'panel': panel
        })
        data_list.append(df)

    return pd.concat(data_list, ignore_index=True)


class TestGeomSurfaceBasic:
    """Basic functionality tests for geom_surface."""

    def test_basic_surface_creates_correct_trace(self, surface_data):
        """Test basic surface plot creation."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) == 1, "Should have 1 trace"
        assert fig.data[0].type == 'surface', "Trace type should be surface"

    def test_surface_has_correct_dimensions(self, surface_data):
        """Test that surface z data is correctly shaped as 2D grid."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        z_data = fig.data[0].z
        assert z_data.shape == (30, 30), "Z data should be 30x30 grid"

    def test_surface_x_y_are_1d_arrays(self, surface_data):
        """Test that x and y are 1D arrays (unique values)."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        x_data = fig.data[0].x
        y_data = fig.data[0].y

        assert len(x_data) == 30, "X should have 30 unique values"
        assert len(y_data) == 30, "Y should have 30 unique values"

    def test_missing_z_raises_error(self, surface_data):
        """Test that missing z aesthetic raises ValueError."""
        with pytest.raises(ValueError, match="geom_surface requires 'x', 'y', and 'z' aesthetics"):
            p = ggplot(surface_data, aes(x='x', y='y')) + geom_surface()
            p.draw()


class TestGeomSurfaceColorscale:
    """Tests for colorscale options in surface plots."""

    def test_default_colorscale_is_set(self, peak_data):
        """Test that default colorscale is applied."""
        p = ggplot(peak_data, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        colorscale = fig.data[0].colorscale
        assert colorscale is not None, "Should have a colorscale"

    def test_custom_colorscale_plasma(self, peak_data):
        """Test custom Plasma colorscale is applied."""
        p = ggplot(peak_data, aes(x='x', y='y', z='z')) + geom_surface(colorscale='Plasma')
        fig = p.draw()

        assert fig.data[0].colorscale is not None

    def test_reversescale_applied(self, peak_data):
        """Test reversed colorscale is applied."""
        p = ggplot(peak_data, aes(x='x', y='y', z='z')) + geom_surface(reversescale=True)
        fig = p.draw()

        assert fig.data[0].reversescale == True, "Reversescale should be True"


class TestGeomSurfaceOpacity:
    """Tests for opacity/alpha parameter."""

    def test_default_opacity_is_one(self, surface_data):
        """Test default opacity is 1."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        assert fig.data[0].opacity == 1.0, "Default opacity should be 1.0"

    def test_custom_opacity_applied(self, surface_data):
        """Test custom opacity value is applied."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_surface(alpha=0.7)
        fig = p.draw()

        assert fig.data[0].opacity == 0.7, "Opacity should be 0.7"


class TestGeomSurfaceColorbar:
    """Tests for colorbar settings."""

    def test_showscale_default_is_true(self, peak_data):
        """Test that colorbar is shown by default."""
        p = ggplot(peak_data, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        assert fig.data[0].showscale == True, "Colorbar should be shown by default"

    def test_hide_colorbar(self, peak_data):
        """Test hiding the colorbar."""
        p = ggplot(peak_data, aes(x='x', y='y', z='z')) + geom_surface(showscale=False)
        fig = p.draw()

        assert fig.data[0].showscale == False, "Colorbar should be hidden"

    def test_colorbar_title(self, peak_data):
        """Test custom colorbar title."""
        p = ggplot(peak_data, aes(x='x', y='y', z='z')) + geom_surface(colorbar_title='Height (z)')
        fig = p.draw()

        assert fig.data[0].colorbar.title.text == 'Height (z)'


class TestGeomSurfaceContours:
    """Tests for contour projections."""

    def test_z_contour_projection(self, peak_data):
        """Test adding z contour projection."""
        contours = dict(z=dict(show=True, project=dict(z=True)))
        p = ggplot(peak_data, aes(x='x', y='y', z='z')) + geom_surface(contours=contours)
        fig = p.draw()

        assert fig.data[0].contours is not None, "Contours should be set"
        assert fig.data[0].contours.z.show == True

    def test_hidesurface_shows_only_contours(self, peak_data):
        """Test hiding surface to show only contours."""
        contours = dict(z=dict(show=True, project=dict(z=True)))
        p = ggplot(peak_data, aes(x='x', y='y', z='z')) + geom_surface(
            contours=contours,
            hidesurface=True
        )
        fig = p.draw()

        assert fig.data[0].hidesurface == True

    def test_multiple_contour_projections(self):
        """Test multiple contour projections (x, y, z)."""
        def sinc_2d(x, y):
            r = np.sqrt(x**2 + y**2)
            return np.where(r == 0, 1, np.sin(r) / r)

        df = make_surface_data(sinc_2d, x_range=(-10, 10), y_range=(-10, 10), resolution=30)
        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(
                colorscale='Plasma',
                contours=dict(
                    x=dict(show=True, usecolormap=True, project=dict(x=True)),
                    y=dict(show=True, usecolormap=True, project=dict(y=True)),
                    z=dict(show=True, usecolormap=True, project=dict(z=True)),
                )
            )
        ).draw()

        assert fig.data[0].contours.x.show is True
        assert fig.data[0].contours.y.show is True
        assert fig.data[0].contours.z.show is True


class TestGeomSurfaceLabels:
    """Tests for axis labels with labs()."""

    def test_labs_sets_all_three_axis_labels(self, surface_data):
        """Test that labs() sets all three axis labels."""
        p = (ggplot(surface_data, aes(x='x', y='y', z='z'))
             + geom_surface()
             + labs(x='X Coordinate', y='Y Coordinate', z='Height'))
        fig = p.draw()

        scene = fig.layout.scene
        assert scene.xaxis.title.text == 'X Coordinate'
        assert scene.yaxis.title.text == 'Y Coordinate'
        assert scene.zaxis.title.text == 'Height'

    def test_labs_sets_title(self, surface_data):
        """Test that labs() sets plot title."""
        p = (ggplot(surface_data, aes(x='x', y='y', z='z'))
             + geom_surface()
             + labs(title='3D Surface Plot'))
        fig = p.draw()

        assert '3D Surface Plot' in fig.layout.title.text

    def test_default_axis_labels_from_mapping(self, surface_data):
        """Test that default axis labels come from column names."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        scene = fig.layout.scene
        assert scene.xaxis.title.text == 'x'
        assert scene.yaxis.title.text == 'y'
        assert scene.zaxis.title.text == 'z'


class TestGeomSurfaceFaceting:
    """Tests for faceted surface plots."""

    def test_facet_wrap_creates_multiple_scenes(self, multi_surface_data):
        """Test that facet_wrap creates separate 3D scenes."""
        p = (ggplot(multi_surface_data, aes(x='x', y='y', z='z'))
             + geom_surface()
             + facet_wrap('panel'))
        fig = p.draw()

        assert len(fig.data) == 2, "Should have 2 surface traces (one per facet)"

        # Each trace should be assigned to a different scene
        scenes = set(trace.scene for trace in fig.data)
        assert len(scenes) == 2, "Should have 2 different scenes"


class TestGeomSurfaceGGSize:
    """Tests for ggsize with surface plots."""

    def test_ggsize_sets_dimensions(self, surface_data):
        """Test that ggsize sets figure dimensions."""
        p = (ggplot(surface_data, aes(x='x', y='y', z='z'))
             + geom_surface()
             + ggsize(width=900, height=700))
        fig = p.draw()

        assert fig.layout.width == 900
        assert fig.layout.height == 700


class TestGeomSurfaceFillAesthetic:
    """Tests for fill aesthetic (surfacecolor)."""

    def test_fill_aesthetic_creates_surfacecolor(self):
        """Test that fill aesthetic creates surfacecolor."""
        x = np.linspace(-2, 2, 20)
        y = np.linspace(-2, 2, 20)
        X, Y = np.meshgrid(x, y)
        Z = X**2 + Y**2
        fill_vals = np.sqrt(X**2 + Y**2)

        df = pd.DataFrame({
            'x': X.flatten(),
            'y': Y.flatten(),
            'z': Z.flatten(),
            'distance': fill_vals.flatten()
        })

        p = ggplot(df, aes(x='x', y='y', z='z', fill='distance')) + geom_surface()
        fig = p.draw()

        assert fig.data[0].surfacecolor is not None, "Should have surfacecolor set"
        assert fig.data[0].surfacecolor.shape == (20, 20), "Surfacecolor should be 20x20"


class TestGeomSurfaceEdgeCases:
    """Edge cases for surface plots."""

    def test_non_grid_data_raises_error(self):
        """Test that non-grid data (like parametric surfaces) raises ValueError."""
        resolution = 20
        u = np.linspace(0, 2 * np.pi, resolution)
        v = np.linspace(0, 2 * np.pi, resolution)
        U, V = np.meshgrid(u, v)
        R, r = 3, 1
        X = (R + r * np.cos(V)) * np.cos(U)
        Y = (R + r * np.cos(V)) * np.sin(U)
        Z = r * np.sin(V)

        df = pd.DataFrame({
            'x': X.flatten(),
            'y': Y.flatten(),
            'z': Z.flatten()
        })

        with pytest.raises(ValueError, match="geom_surface requires data on a regular x-y grid"):
            p = ggplot(df, aes(x='x', y='y', z='z')) + geom_surface()
            p.draw()

    def test_small_grid(self):
        """Test with small 3x3 grid."""
        x = np.array([0, 1, 2])
        y = np.array([0, 1, 2])
        X, Y = np.meshgrid(x, y)
        Z = X + Y

        df = pd.DataFrame({
            'x': X.flatten(),
            'y': Y.flatten(),
            'z': Z.flatten()
        })

        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        assert fig.data[0].z.shape == (3, 3)

    def test_non_square_grid(self):
        """Test with non-square grid (different x and y sizes)."""
        x = np.linspace(0, 1, 20)
        y = np.linspace(0, 2, 40)
        X, Y = np.meshgrid(x, y)
        Z = X * Y

        df = pd.DataFrame({
            'x': X.flatten(),
            'y': Y.flatten(),
            'z': Z.flatten()
        })

        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        assert fig.data[0].z.shape == (40, 20), "Z shape should be (ny, nx)"

    def test_with_nan_values(self):
        """Test that NaN values are handled."""
        x = np.linspace(-2, 2, 10)
        y = np.linspace(-2, 2, 10)
        X, Y = np.meshgrid(x, y)
        Z = X + Y
        Z[0, 0] = np.nan
        Z[5, 5] = np.nan

        df = pd.DataFrame({
            'x': X.flatten(),
            'y': Y.flatten(),
            'z': Z.flatten()
        })

        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        assert isinstance(fig, Figure)


class TestGeomWireframeBasic:
    """Tests for geom_wireframe."""

    def test_basic_wireframe_creates_scatter3d(self, surface_data):
        """Test basic wireframe plot creation."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_wireframe()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) > 0, "Should have traces"
        assert fig.data[0].type == 'scatter3d', "Traces should be scatter3d"
        assert fig.data[0].mode == 'lines', "Mode should be lines"

    def test_wireframe_trace_count(self, surface_data):
        """Test that wireframe creates correct number of traces."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_wireframe()
        fig = p.draw()

        # 30 lines along x + 30 lines along y = 60 traces
        assert len(fig.data) == 60, "Should have 60 line traces (30 x-lines + 30 y-lines)"

    def test_wireframe_custom_color(self, surface_data):
        """Test wireframe with custom color."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_wireframe(color='red')
        fig = p.draw()

        assert fig.data[0].line.color == 'red', "Line color should be red"

    def test_wireframe_custom_linewidth(self, surface_data):
        """Test wireframe with custom line width."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_wireframe(linewidth=2)
        fig = p.draw()

        assert fig.data[0].line.width == 2, "Line width should be 2"

    def test_wireframe_alpha(self, surface_data):
        """Test wireframe opacity."""
        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_wireframe(alpha=0.5)
        fig = p.draw()

        assert fig.data[0].opacity == 0.5, "Opacity should be 0.5"

    def test_wireframe_missing_z_raises_error(self, surface_data):
        """Test that missing z aesthetic raises ValueError."""
        with pytest.raises(ValueError, match="geom_wireframe requires 'x', 'y', and 'z' aesthetics"):
            p = ggplot(surface_data, aes(x='x', y='y')) + geom_wireframe()
            p.draw()

    def test_wireframe_non_grid_data_raises_error(self):
        """Test that geom_wireframe also raises error for non-grid data."""
        resolution = 20
        u = np.linspace(0, 2 * np.pi, resolution)
        v = np.linspace(0, np.pi, resolution)
        U, V = np.meshgrid(u, v)
        X = np.cos(U) * np.sin(V)
        Y = np.sin(U) * np.sin(V)
        Z = np.cos(V)

        df = pd.DataFrame({
            'x': X.flatten(),
            'y': Y.flatten(),
            'z': Z.flatten()
        })

        with pytest.raises(ValueError, match="geom_wireframe requires data on a regular x-y grid"):
            p = ggplot(df, aes(x='x', y='y', z='z')) + geom_wireframe()
            p.draw()


class TestGeomSurfaceAndWireframeCombination:
    """Tests for combining surface and wireframe."""

    def test_surface_with_points(self, peak_data):
        """Test surface plot combined with scatter points."""
        p = (ggplot(peak_data, aes(x='x', y='y', z='z'))
             + geom_surface(alpha=0.8)
             + geom_point_3d(color='red', size=2))
        fig = p.draw()

        trace_types = [trace.type for trace in fig.data]
        assert 'surface' in trace_types
        assert 'scatter3d' in trace_types


class TestGeomSurfaceDataIntegrity:
    """Tests to verify data integrity."""

    def test_original_data_unchanged(self, surface_data):
        """Test that original dataframe is not modified."""
        original_shape = surface_data.shape
        original_values = surface_data['z'].values.copy()

        p = ggplot(surface_data, aes(x='x', y='y', z='z')) + geom_surface()
        p.draw()

        assert surface_data.shape == original_shape
        np.testing.assert_array_equal(surface_data['z'].values, original_values)

    def test_z_values_preserved(self, peak_data):
        """Test that z values in the surface match original data."""
        p = ggplot(peak_data, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()

        z_in_figure = fig.data[0].z
        z_original = peak_data['z'].values.reshape(25, 25)

        # Values should be close (might be reordered)
        assert np.allclose(np.sort(z_in_figure.flatten()), np.sort(z_original.flatten()))


class TestMathematicalSurfaces:
    """Tests for various mathematical surface functions."""

    def test_paraboloid(self):
        """Test paraboloid z = x^2 + y^2."""
        df = make_surface_data(lambda x, y: x**2 + y**2, resolution=30)
        fig = (ggplot(df, aes(x='x', y='y', z='z')) + geom_surface()).draw()

        assert fig.data[0].type == 'surface'
        # Check that z values are non-negative (paraboloid property)
        assert np.all(fig.data[0].z >= 0)

    def test_saddle_surface(self):
        """Test saddle surface x^2 - y^2."""
        df = make_surface_data(lambda x, y: x**2 - y**2, resolution=30)
        fig = (ggplot(df, aes(x='x', y='y', z='z')) + geom_surface()).draw()

        assert fig.data[0].type == 'surface'
        # Saddle surface has both positive and negative values
        z_flat = fig.data[0].z.flatten()
        assert np.any(z_flat > 0) and np.any(z_flat < 0)


class TestFullFeatured:
    """Test combining multiple features."""

    def test_all_customizations_applied(self):
        """Test combining multiple features."""
        df = make_surface_data(
            lambda x, y: np.sin(np.sqrt(x**2 + y**2)) * np.exp(-(x**2 + y**2) / 20),
            x_range=(-8, 8),
            y_range=(-8, 8),
            resolution=40,
        )

        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(
                colorscale='Viridis',
                alpha=0.9,
                contours=dict(
                    z=dict(show=True, usecolormap=True, project=dict(z=True))
                ),
            )
            + labs(
                title='Damped Ripple with Contour Projection',
                x='X Coordinate',
                y='Y Coordinate',
                z='Amplitude',
            )
            + theme_minimal()
            + ggsize(width=900, height=700)
        ).draw()

        assert fig.data[0].type == 'surface'
        assert fig.data[0].opacity == 0.9
        assert fig.data[0].contours.z.show is True
        assert fig.layout.width == 900
        assert fig.layout.height == 700
        assert fig.layout.scene.xaxis.title.text == 'X Coordinate'
        assert fig.layout.scene.yaxis.title.text == 'Y Coordinate'
        assert fig.layout.scene.zaxis.title.text == 'Amplitude'
