# test_geom_surface_examples.py
# Tests that validate all examples from geom_surface_examples.py work correctly

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.graph_objects import Figure

from ggplotly import (
    ggplot, aes, geom_surface, geom_wireframe, geom_point_3d,
    facet_wrap, facet_grid,
    theme_minimal, theme_dark, theme_classic, theme_ggplot2,
    labs,
    ggsize,
)


# Helper function from examples file
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


class TestBasicSurfaces:
    """Test basic surface plot examples."""

    def test_paraboloid(self):
        """Example 1: Simple paraboloid z = x^2 + y^2."""
        df = make_surface_data(lambda x, y: x**2 + y**2)
        fig = (ggplot(df, aes(x='x', y='y', z='z')) + geom_surface()).draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'surface'

    def test_sinc_function(self):
        """Example 2: Sinc function."""
        def sinc_2d(x, y):
            r = np.sqrt(x**2 + y**2)
            return np.where(r == 0, 1, np.sin(r) / r)

        df = make_surface_data(sinc_2d, x_range=(-10, 10), y_range=(-10, 10), resolution=40)
        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface()
            + labs(title='2D Sinc Function')
        ).draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'surface'

    def test_ripple_pattern(self):
        """Example 2: Ripple pattern sin(x) * cos(y)."""
        df = make_surface_data(lambda x, y: np.sin(x) * np.cos(y))
        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface()
            + labs(title='Ripple Pattern: sin(x) * cos(y)')
        ).draw()

        assert isinstance(fig, Figure)

    def test_saddle_surface(self):
        """Example 2: Saddle surface x^2 - y^2."""
        df = make_surface_data(lambda x, y: x**2 - y**2)
        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface()
            + labs(title='Saddle Surface: x² - y²')
        ).draw()

        assert isinstance(fig, Figure)


class TestColorscales:
    """Test colorscale examples."""

    @pytest.fixture
    def paraboloid_data(self):
        return make_surface_data(lambda x, y: x**2 + y**2, resolution=30)

    def test_viridis(self, paraboloid_data):
        """Example 3: Viridis colorscale."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Viridis')
        ).draw()

        assert fig.data[0].colorscale is not None

    def test_plasma(self, paraboloid_data):
        """Example 3: Plasma colorscale."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Plasma')
        ).draw()

        assert isinstance(fig, Figure)

    def test_blues(self, paraboloid_data):
        """Example 3: Blues colorscale."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Blues')
        ).draw()

        assert isinstance(fig, Figure)

    def test_rdbu_diverging(self):
        """Example 3: RdBu diverging colorscale for saddle."""
        df = make_surface_data(lambda x, y: x**2 - y**2, resolution=30)
        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='RdBu')
        ).draw()

        assert isinstance(fig, Figure)

    def test_hot(self, paraboloid_data):
        """Example 3: Hot colorscale."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Hot')
        ).draw()

        assert isinstance(fig, Figure)

    def test_earth(self, paraboloid_data):
        """Example 3: Earth colorscale."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Earth')
        ).draw()

        assert isinstance(fig, Figure)

    def test_reversed(self, paraboloid_data):
        """Example 3: Reversed colorscale."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Viridis', reversescale=True)
        ).draw()

        assert fig.data[0].reversescale is True


class TestOpacity:
    """Test opacity/transparency examples."""

    @pytest.fixture
    def paraboloid_data(self):
        return make_surface_data(lambda x, y: x**2 + y**2, resolution=30)

    def test_semi_transparent(self, paraboloid_data):
        """Example 4: Semi-transparent surface."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(alpha=0.7, colorscale='Plasma')
        ).draw()

        assert fig.data[0].opacity == 0.7

    def test_highly_transparent(self, paraboloid_data):
        """Example 4: Highly transparent surface."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(alpha=0.4, colorscale='Blues')
        ).draw()

        assert fig.data[0].opacity == 0.4


class TestContours:
    """Test contour projection examples."""

    @pytest.fixture
    def paraboloid_data(self):
        return make_surface_data(lambda x, y: x**2 + y**2, resolution=30)

    def test_z_contour_projection(self, paraboloid_data):
        """Example 5: Z-axis contour projection."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(
                colorscale='Viridis',
                contours=dict(
                    z=dict(show=True, usecolormap=True, project=dict(z=True))
                )
            )
        ).draw()

        assert fig.data[0].contours is not None
        assert fig.data[0].contours.z.show is True

    def test_multiple_contours(self):
        """Example 5: Multiple contour projections."""
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

    def test_contours_only(self, paraboloid_data):
        """Example 5: Show only contours (hide surface)."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(
                hidesurface=True,
                contours=dict(
                    z=dict(show=True, usecolormap=True, project=dict(z=True))
                )
            )
        ).draw()

        assert fig.data[0].hidesurface is True


class TestColorbar:
    """Test colorbar customization examples."""

    @pytest.fixture
    def paraboloid_data(self):
        return make_surface_data(lambda x, y: x**2 + y**2, resolution=30)

    def test_hide_colorbar(self, paraboloid_data):
        """Example 6: Hide colorbar."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(showscale=False)
        ).draw()

        assert fig.data[0].showscale is False

    def test_colorbar_title(self, paraboloid_data):
        """Example 6: Custom colorbar title."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(colorbar_title='Height (z)')
        ).draw()

        assert fig.data[0].colorbar.title.text == 'Height (z)'


class TestWireframe:
    """Test wireframe examples."""

    @pytest.fixture
    def paraboloid_data(self):
        return make_surface_data(lambda x, y: x**2 + y**2, resolution=20)

    def test_basic_wireframe(self, paraboloid_data):
        """Example 7: Basic wireframe."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_wireframe()
        ).draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'scatter3d'
        assert fig.data[0].mode == 'lines'

    def test_custom_color(self, paraboloid_data):
        """Example 7: Wireframe with custom color."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_wireframe(color='darkblue', linewidth=1.5)
        ).draw()

        assert fig.data[0].line.color == 'darkblue'
        assert fig.data[0].line.width == 1.5

    def test_transparent_wireframe(self):
        """Example 7: Wireframe with transparency."""
        def sinc_2d(x, y):
            r = np.sqrt(x**2 + y**2)
            return np.where(r == 0, 1, np.sin(r) / r)

        df = make_surface_data(sinc_2d, x_range=(-10, 10), y_range=(-10, 10), resolution=20)
        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_wireframe(color='purple', alpha=0.6)
        ).draw()

        assert fig.data[0].opacity == 0.6


class TestSurfaceWithPoints:
    """Test combining surface with points."""

    def test_surface_with_points(self):
        """Example 8: Surface with overlaid sample points."""
        df_surface = make_surface_data(lambda x, y: x**2 + y**2, resolution=25)

        np.random.seed(123)
        sample_x = np.random.uniform(-4, 4, 30)
        sample_y = np.random.uniform(-4, 4, 30)
        sample_z = sample_x**2 + sample_y**2 + np.random.randn(30) * 2
        df_points = pd.DataFrame({'x': sample_x, 'y': sample_y, 'z': sample_z})

        fig = (
            ggplot(df_surface, aes(x='x', y='y', z='z'))
            + geom_surface(alpha=0.6, colorscale='Blues')
            + geom_point_3d(data=df_points, size=8, color='red')
        ).draw()

        trace_types = [trace.type for trace in fig.data]
        assert 'surface' in trace_types
        assert 'scatter3d' in trace_types


class TestFillAesthetic:
    """Test fill aesthetic (surfacecolor) examples."""

    def test_fill_by_angle(self):
        """Example 9: Surface colored by angle instead of height."""
        df = make_surface_data(lambda x, y: np.sin(np.sqrt(x**2 + y**2)), resolution=30)
        df['angle'] = np.arctan2(df['y'], df['x'])

        fig = (
            ggplot(df, aes(x='x', y='y', z='z', fill='angle'))
            + geom_surface(colorscale='Rainbow')
        ).draw()

        assert fig.data[0].surfacecolor is not None

    def test_fill_by_radius(self):
        """Example 9: Gaussian surface colored by radius."""
        df = make_surface_data(lambda x, y: np.exp(-(x**2 + y**2) / 10), resolution=30)
        df['intensity'] = np.sqrt(df['x']**2 + df['y']**2)

        fig = (
            ggplot(df, aes(x='x', y='y', z='z', fill='intensity'))
            + geom_surface(colorscale='Viridis')
        ).draw()

        assert fig.data[0].surfacecolor is not None


class TestThemes:
    """Test theme examples."""

    @pytest.fixture
    def paraboloid_data(self):
        return make_surface_data(lambda x, y: x**2 + y**2, resolution=25)

    def test_minimal_theme(self, paraboloid_data):
        """Example 10: Minimal theme."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Plasma')
            + theme_minimal()
        ).draw()

        assert isinstance(fig, Figure)

    def test_dark_theme(self):
        """Example 10: Dark theme."""
        def sinc_2d(x, y):
            r = np.sqrt(x**2 + y**2)
            return np.where(r == 0, 1, np.sin(r) / r)

        df = make_surface_data(sinc_2d, x_range=(-10, 10), y_range=(-10, 10), resolution=30)
        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Inferno')
            + theme_dark()
        ).draw()

        assert isinstance(fig, Figure)

    def test_classic_theme(self, paraboloid_data):
        """Example 10: Classic theme."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Blues')
            + theme_classic()
        ).draw()

        assert isinstance(fig, Figure)

    def test_ggplot2_theme(self, paraboloid_data):
        """Example 10: ggplot2 theme."""
        fig = (
            ggplot(paraboloid_data, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Viridis')
            + theme_ggplot2()
        ).draw()

        assert isinstance(fig, Figure)


class TestLabels:
    """Test labs() examples."""

    def test_custom_axis_labels(self):
        """Example 11: Custom axis labels."""
        df = make_surface_data(lambda x, y: x**2 + y**2, resolution=25)
        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface()
            + labs(
                title='Paraboloid Surface',
                x='X Coordinate',
                y='Y Coordinate',
                z='Height (z = x² + y²)',
            )
        ).draw()

        assert fig.layout.scene.xaxis.title.text == 'X Coordinate'
        assert fig.layout.scene.yaxis.title.text == 'Y Coordinate'
        assert fig.layout.scene.zaxis.title.text == 'Height (z = x² + y²)'


class TestGGSize:
    """Test ggsize() examples."""

    def test_custom_size(self):
        """Example 12: Custom figure size."""
        def sinc_2d(x, y):
            r = np.sqrt(x**2 + y**2)
            return np.where(r == 0, 1, np.sin(r) / r)

        df = make_surface_data(sinc_2d, x_range=(-10, 10), y_range=(-10, 10), resolution=30)
        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Plasma')
            + labs(title='Large 3D Surface')
            + ggsize(width=900, height=700)
        ).draw()

        assert fig.layout.width == 900
        assert fig.layout.height == 700


class TestFaceting:
    """Test faceting examples."""

    def test_facet_wrap(self):
        """Example 13: Faceted surface plots."""
        def make_gaussian(center_x, center_y, sigma, label):
            df = make_surface_data(
                lambda x, y: np.exp(-((x - center_x)**2 + (y - center_y)**2) / (2 * sigma**2)),
                x_range=(-5, 5),
                y_range=(-5, 5),
                resolution=20,
            )
            df['type'] = label
            return df

        df = pd.concat([
            make_gaussian(0, 0, 1.0, 'Narrow'),
            make_gaussian(0, 0, 2.0, 'Medium'),
            make_gaussian(0, 0, 3.0, 'Wide'),
        ], ignore_index=True)

        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Viridis')
            + facet_wrap('type')
        ).draw()

        assert isinstance(fig, Figure)
        # Should have 3 surface traces
        surface_traces = [t for t in fig.data if t.type == 'surface']
        assert len(surface_traces) == 3


class TestRealWorldExamples:
    """Test real-world example scenarios."""

    def test_terrain(self):
        """Example 14: Simulated terrain."""
        np.random.seed(42)

        def generate_terrain(size=30):
            x = np.linspace(0, 10, size)
            y = np.linspace(0, 10, size)
            X, Y = np.meshgrid(x, y)
            Z = (
                2 * np.sin(0.5 * X) * np.cos(0.5 * Y) +
                1 * np.sin(1.0 * X + 0.5) * np.cos(0.8 * Y) +
                0.5 * np.sin(2.0 * X) * np.cos(2.0 * Y)
            )
            Z = Z - Z.min()
            return pd.DataFrame({
                'longitude': X.flatten(),
                'latitude': Y.flatten(),
                'elevation': Z.flatten(),
            })

        df = generate_terrain()
        fig = (
            ggplot(df, aes(x='longitude', y='latitude', z='elevation'))
            + geom_surface(colorscale='Earth')
            + labs(title='Simulated Terrain')
            + theme_minimal()
        ).draw()

        assert isinstance(fig, Figure)

    def test_bivariate_normal(self):
        """Example 15: Bivariate normal distribution."""
        def bivariate_normal(x, y, mu_x=0, mu_y=0, sigma_x=1, sigma_y=1, rho=0):
            z = (
                ((x - mu_x) / sigma_x)**2
                - 2 * rho * ((x - mu_x) / sigma_x) * ((y - mu_y) / sigma_y)
                + ((y - mu_y) / sigma_y)**2
            )
            return np.exp(-z / (2 * (1 - rho**2))) / (2 * np.pi * sigma_x * sigma_y * np.sqrt(1 - rho**2))

        df = make_surface_data(
            lambda x, y: bivariate_normal(x, y, sigma_x=1.5, sigma_y=1.0, rho=0.5),
            x_range=(-4, 4),
            y_range=(-4, 4),
            resolution=40,
        )

        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Viridis')
            + labs(title='Bivariate Normal Distribution')
            + theme_minimal()
        ).draw()

        assert isinstance(fig, Figure)

    def test_response_surface(self):
        """Example 16: Response surface optimization."""
        def response_surface(x, y):
            return 10 - (x - 2)**2 - (y + 1)**2 + 0.5 * np.sin(3 * x) * np.cos(3 * y)

        df = make_surface_data(response_surface, x_range=(-2, 6), y_range=(-5, 3), resolution=30)
        optimal_idx = df['z'].idxmax()
        optimal_point = df.loc[[optimal_idx]]

        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(alpha=0.8, colorscale='RdYlGn')
            + geom_point_3d(data=optimal_point, size=12, color='black')
            + labs(title='Response Surface Optimization')
            + theme_minimal()
        ).draw()

        trace_types = [trace.type for trace in fig.data]
        assert 'surface' in trace_types
        assert 'scatter3d' in trace_types

    def test_temperature_field(self):
        """Example 21: Temperature distribution."""
        def temperature_field(x, y):
            r = np.sqrt(x**2 + y**2)
            return 100 * np.exp(-r / 3) + 20

        df = make_surface_data(temperature_field, x_range=(-10, 10), y_range=(-10, 10), resolution=30)

        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Hot')
            + labs(title='Temperature Distribution')
            + theme_minimal()
        ).draw()

        assert isinstance(fig, Figure)

    def test_wave_interference(self):
        """Example 22: Wave interference pattern."""
        def wave_interference(x, y, source1=(-3, 0), source2=(3, 0), wavelength=1):
            k = 2 * np.pi / wavelength
            r1 = np.sqrt((x - source1[0])**2 + (y - source1[1])**2)
            r2 = np.sqrt((x - source2[0])**2 + (y - source2[1])**2)
            return np.cos(k * r1) + np.cos(k * r2)

        df = make_surface_data(
            lambda x, y: wave_interference(x, y, wavelength=2),
            x_range=(-10, 10),
            y_range=(-10, 10),
            resolution=40,
        )

        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='RdBu')
            + labs(title='Two-Source Wave Interference')
            + theme_dark()
        ).draw()

        assert isinstance(fig, Figure)

    def test_rosenbrock_function(self):
        """Example 23: Cost function (Rosenbrock)."""
        def cost_function(x, y):
            return (1 - x)**2 + 100 * (y - x**2)**2

        df = make_surface_data(cost_function, x_range=(-2, 2), y_range=(-1, 3), resolution=40)
        df['log_cost'] = np.log10(df['z'] + 1)

        fig = (
            ggplot(df, aes(x='x', y='y', z='log_cost'))
            + geom_surface(colorscale='Inferno')
            + labs(title='Rosenbrock Function (Log Scale)')
            + theme_minimal()
        ).draw()

        assert isinstance(fig, Figure)


class TestParametricSurfaces:
    """Test parametric surfaces using Plotly directly."""

    def test_torus(self):
        """Example 17: Torus using Plotly directly."""
        resolution = 30
        u = np.linspace(0, 2 * np.pi, resolution)
        v = np.linspace(0, 2 * np.pi, resolution)
        U, V = np.meshgrid(u, v)
        R, r = 3, 1
        X = (R + r * np.cos(V)) * np.cos(U)
        Y = (R + r * np.cos(V)) * np.sin(U)
        Z = r * np.sin(V)

        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Rainbow')])
        fig.update_layout(title='Torus', scene=dict(aspectmode='data'))

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'surface'
        assert fig.data[0].x.shape == (resolution, resolution)

    def test_sphere(self):
        """Example 18: Sphere using Plotly directly."""
        resolution = 30
        u = np.linspace(0, 2 * np.pi, resolution)
        v = np.linspace(0, np.pi, resolution)
        U, V = np.meshgrid(u, v)
        radius = 1
        X = radius * np.cos(U) * np.sin(V)
        Y = radius * np.sin(U) * np.sin(V)
        Z = radius * np.cos(V)

        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Blues')])
        fig.update_layout(title='Sphere', scene=dict(aspectmode='data'))

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'surface'

    def test_helicoid(self):
        """Example 19: Helicoid using Plotly directly."""
        resolution = 30
        u = np.linspace(-2, 2, resolution)
        v = np.linspace(0, 4 * np.pi, resolution)
        U, V = np.meshgrid(u, v)
        X = U * np.cos(V)
        Y = U * np.sin(V)
        Z = V / 2

        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
        fig.update_layout(title='Helicoid')

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'surface'


class TestNonSquareGrids:
    """Test non-square grid examples."""

    def test_rectangular_grid(self):
        """Example 24: Non-square grid surface."""
        x = np.linspace(-10, 10, 50)  # Wide
        y = np.linspace(-2, 2, 10)    # Narrow
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.exp(-Y**2)

        df = pd.DataFrame({
            'x': X.flatten(),
            'y': Y.flatten(),
            'z': Z.flatten(),
        })

        fig = (
            ggplot(df, aes(x='x', y='y', z='z'))
            + geom_surface(colorscale='Plasma')
            + labs(title='Non-Square Grid Surface')
        ).draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].z.shape == (10, 50)  # (ny, nx)


class TestCombinedFeatures:
    """Test combining multiple features."""

    def test_full_featured(self):
        """Example 25: Combining multiple features."""
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

        assert isinstance(fig, Figure)
        assert fig.data[0].opacity == 0.9
        assert fig.data[0].contours.z.show is True
        assert fig.layout.width == 900
        assert fig.layout.height == 700
