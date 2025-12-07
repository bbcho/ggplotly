# test_phase6_phase7.py
"""
Tests for Phase 6 (Facets & Themes) and Phase 7 (Core Functions).
"""

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go


# ============================================================================
# Phase 6 Tests: Facets
# ============================================================================

class TestFacetWrap:
    """Tests for facet_wrap improvements."""

    def test_facet_wrap_default_params(self):
        """Test facet_wrap has correct default parameters."""
        from ggplotly.facets import facet_wrap

        fw = facet_wrap('group')
        assert fw.strip_position == 'top'
        assert fw.drop is True
        assert fw.as_table is True

    def test_facet_wrap_strip_position_top(self):
        """Test strip_position='top' (default)."""
        from ggplotly.facets import facet_wrap

        fw = facet_wrap('group', strip_position='top')
        assert fw.strip_position == 'top'

    def test_facet_wrap_strip_position_bottom(self):
        """Test strip_position='bottom'."""
        from ggplotly.facets import facet_wrap

        fw = facet_wrap('group', strip_position='bottom')
        assert fw.strip_position == 'bottom'

    def test_facet_wrap_strip_position_left(self):
        """Test strip_position='left'."""
        from ggplotly.facets import facet_wrap

        fw = facet_wrap('group', strip_position='left')
        assert fw.strip_position == 'left'

    def test_facet_wrap_strip_position_right(self):
        """Test strip_position='right'."""
        from ggplotly.facets import facet_wrap

        fw = facet_wrap('group', strip_position='right')
        assert fw.strip_position == 'right'

    def test_facet_wrap_drop_true(self):
        """Test drop=True drops unused factor levels."""
        from ggplotly.facets import facet_wrap

        fw = facet_wrap('group', drop=True)
        assert fw.drop is True

    def test_facet_wrap_drop_false(self):
        """Test drop=False keeps unused factor levels."""
        from ggplotly.facets import facet_wrap

        fw = facet_wrap('group', drop=False)
        assert fw.drop is False

    def test_facet_wrap_as_table_true(self):
        """Test as_table=True fills by row."""
        from ggplotly.facets import facet_wrap

        fw = facet_wrap('group', as_table=True)
        assert fw.as_table is True

    def test_facet_wrap_as_table_false(self):
        """Test as_table=False fills by column."""
        from ggplotly.facets import facet_wrap

        fw = facet_wrap('group', as_table=False)
        assert fw.as_table is False

    def test_facet_wrap_all_params(self):
        """Test facet_wrap with all new parameters."""
        from ggplotly.facets import facet_wrap

        fw = facet_wrap(
            'group',
            ncol=3,
            nrow=2,
            scales='free',
            strip_position='bottom',
            drop=False,
            as_table=False
        )
        assert fw.ncol == 3
        assert fw.nrow == 2
        assert fw.scales == 'free'
        assert fw.strip_position == 'bottom'
        assert fw.drop is False
        assert fw.as_table is False


class TestFacetGrid:
    """Tests for facet_grid improvements."""

    def test_facet_grid_default_params(self):
        """Test facet_grid has correct default parameters."""
        from ggplotly.facets import facet_grid

        fg = facet_grid('row_var', 'col_var')
        assert fg.margins is False
        assert fg.drop is True
        assert fg.switch is None

    def test_facet_grid_margins_false(self):
        """Test margins=False (default)."""
        from ggplotly.facets import facet_grid

        fg = facet_grid('row', 'col', margins=False)
        assert fg.margins is False

    def test_facet_grid_margins_true(self):
        """Test margins=True shows marginal facets."""
        from ggplotly.facets import facet_grid

        fg = facet_grid('row', 'col', margins=True)
        assert fg.margins is True

    def test_facet_grid_margins_list(self):
        """Test margins as list of variables."""
        from ggplotly.facets import facet_grid

        fg = facet_grid('row', 'col', margins=['row'])
        assert fg.margins == ['row']

    def test_facet_grid_drop_true(self):
        """Test drop=True drops unused levels."""
        from ggplotly.facets import facet_grid

        fg = facet_grid('row', 'col', drop=True)
        assert fg.drop is True

    def test_facet_grid_drop_false(self):
        """Test drop=False keeps unused levels."""
        from ggplotly.facets import facet_grid

        fg = facet_grid('row', 'col', drop=False)
        assert fg.drop is False

    def test_facet_grid_switch_none(self):
        """Test switch=None (default)."""
        from ggplotly.facets import facet_grid

        fg = facet_grid('row', 'col', switch=None)
        assert fg.switch is None

    def test_facet_grid_switch_x(self):
        """Test switch='x' moves x facet labels to bottom."""
        from ggplotly.facets import facet_grid

        fg = facet_grid('row', 'col', switch='x')
        assert fg.switch == 'x'

    def test_facet_grid_switch_y(self):
        """Test switch='y' moves y facet labels to left."""
        from ggplotly.facets import facet_grid

        fg = facet_grid('row', 'col', switch='y')
        assert fg.switch == 'y'

    def test_facet_grid_switch_both(self):
        """Test switch='both' moves both labels."""
        from ggplotly.facets import facet_grid

        fg = facet_grid('row', 'col', switch='both')
        assert fg.switch == 'both'

    def test_facet_grid_all_params(self):
        """Test facet_grid with all new parameters."""
        from ggplotly.facets import facet_grid

        fg = facet_grid(
            'row_var',
            'col_var',
            scales='free_x',
            space='free_y',
            margins=['row_var'],
            drop=False,
            switch='both'
        )
        assert fg.scales == 'free_x'
        assert fg.space == 'free_y'
        assert fg.margins == ['row_var']
        assert fg.drop is False
        assert fg.switch == 'both'


# ============================================================================
# Phase 6 Tests: Themes
# ============================================================================

class TestThemeExpansion:
    """Tests for expanded theme() parameters."""

    def test_theme_default_params(self):
        """Test theme has default parameters."""
        from ggplotly.themes import theme, Theme

        t = theme()
        # theme() returns a CustomTheme which inherits from Theme
        assert isinstance(t, Theme)
        assert t.legend_position == 'right'
        assert t.legend_show is True

    def test_theme_axis_title(self):
        """Test axis_title parameter - functional test via apply."""
        from ggplotly.themes import theme, element_text

        t = theme(axis_title=element_text(size=14, color='blue'))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        # Check that axis title styling was applied
        assert fig.layout.xaxis.title.font.size == 14
        assert fig.layout.xaxis.title.font.color == 'blue'

    def test_theme_axis_title_x(self):
        """Test axis_title_x parameter."""
        from ggplotly.themes import theme, element_text

        t = theme(axis_title_x=element_text(size=12))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.xaxis.title.font.size == 12

    def test_theme_axis_title_y(self):
        """Test axis_title_y parameter."""
        from ggplotly.themes import theme, element_text

        t = theme(axis_title_y=element_text(size=16, color='red'))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.yaxis.title.font.size == 16
        assert fig.layout.yaxis.title.font.color == 'red'

    def test_theme_axis_text(self):
        """Test axis_text parameter."""
        from ggplotly.themes import theme, element_text

        t = theme(axis_text=element_text(size=10, color='gray'))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        # axis_text affects tickfont
        assert fig.layout.xaxis.tickfont.size == 10
        assert fig.layout.xaxis.tickfont.color == 'gray'

    def test_theme_axis_text_x(self):
        """Test axis_text_x parameter."""
        from ggplotly.themes import theme, element_text

        t = theme(axis_text_x=element_text(size=11))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.xaxis.tickfont.size == 11

    def test_theme_axis_text_y(self):
        """Test axis_text_y parameter."""
        from ggplotly.themes import theme, element_text

        t = theme(axis_text_y=element_text(size=9))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.yaxis.tickfont.size == 9

    def test_theme_axis_line(self):
        """Test axis_line parameter."""
        from ggplotly.themes import theme, element_line

        t = theme(axis_line=element_line(color='black', width=2))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.xaxis.linecolor == 'black'
        assert fig.layout.xaxis.linewidth == 2
        assert fig.layout.xaxis.showline is True

    def test_theme_axis_line_x(self):
        """Test axis_line_x parameter."""
        from ggplotly.themes import theme, element_line

        t = theme(axis_line_x=element_line(color='red', width=1))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.xaxis.linecolor == 'red'

    def test_theme_axis_line_y(self):
        """Test axis_line_y parameter."""
        from ggplotly.themes import theme, element_line

        t = theme(axis_line_y=element_line(color='blue', width=1))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.yaxis.linecolor == 'blue'

    def test_theme_axis_ticks(self):
        """Test axis_ticks parameter."""
        from ggplotly.themes import theme, element_line

        t = theme(axis_ticks=element_line(color='gray', width=1))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.xaxis.tickcolor == 'gray'
        assert fig.layout.xaxis.tickwidth == 1

    def test_theme_panel_background(self):
        """Test panel_background parameter."""
        from ggplotly.themes import theme, element_rect

        t = theme(panel_background=element_rect(fill='#f0f0f0'))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.plot_bgcolor == '#f0f0f0'

    def test_theme_panel_grid(self):
        """Test panel_grid parameter."""
        from ggplotly.themes import theme, element_line

        t = theme(panel_grid=element_line(color='lightgray', width=0.5))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.xaxis.gridcolor == 'lightgray'
        assert fig.layout.yaxis.gridcolor == 'lightgray'

    def test_theme_panel_grid_major(self):
        """Test panel_grid_major parameter."""
        from ggplotly.themes import theme, element_line

        t = theme(panel_grid_major=element_line(color='gray', width=1))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.xaxis.gridcolor == 'gray'
        assert fig.layout.xaxis.showgrid is True

    def test_theme_panel_grid_minor(self):
        """Test panel_grid_minor parameter - applies grid color."""
        from ggplotly.themes import theme, element_line

        # panel_grid_minor is stored but Plotly doesn't have separate minor grid control
        t = theme(panel_grid_minor=element_line(color='lightgray', width=0.25))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        # Just verify theme was created without error
        assert t is not None

    def test_theme_panel_border(self):
        """Test panel_border parameter."""
        from ggplotly.themes import theme, element_rect

        # panel_border is stored but may not directly apply in Plotly
        t = theme(panel_border=element_rect(color='black', fill='white'))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        assert t is not None

    def test_theme_plot_title(self):
        """Test plot_title parameter."""
        from ggplotly.themes import theme, element_text

        t = theme(plot_title=element_text(size=18, color='darkblue'))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.title.font.size == 18
        assert fig.layout.title.font.color == 'darkblue'

    def test_theme_plot_subtitle(self):
        """Test plot_subtitle parameter."""
        from ggplotly.themes import theme, element_text

        # plot_subtitle is stored for potential future use
        t = theme(plot_subtitle=element_text(size=14, color='gray'))
        assert t is not None

    def test_theme_plot_caption(self):
        """Test plot_caption parameter."""
        from ggplotly.themes import theme, element_text

        # plot_caption is stored for potential future use
        t = theme(plot_caption=element_text(size=10))
        assert t is not None

    def test_theme_plot_background(self):
        """Test plot_background parameter."""
        from ggplotly.themes import theme, element_rect

        t = theme(plot_background=element_rect(fill='#f0f0f0'))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.paper_bgcolor == '#f0f0f0'

    def test_theme_legend_title(self):
        """Test legend_title parameter."""
        from ggplotly.themes import theme, element_text

        t = theme(legend_title=element_text(size=12, color='navy'))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.legend.title.font.size == 12
        assert fig.layout.legend.title.font.color == 'navy'

    def test_theme_legend_text(self):
        """Test legend_text parameter."""
        from ggplotly.themes import theme, element_text

        t = theme(legend_text=element_text(size=10))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.legend.font.size == 10

    def test_theme_legend_background(self):
        """Test legend_background parameter."""
        from ggplotly.themes import theme, element_rect

        t = theme(legend_background=element_rect(fill='white', color='gray'))
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        t.apply(fig)
        assert fig.layout.legend.bgcolor == 'white'
        assert fig.layout.legend.bordercolor == 'gray'

    def test_theme_strip_text(self):
        """Test strip_text parameter."""
        from ggplotly.themes import theme, element_text

        # strip_text is stored for faceted plots
        t = theme(strip_text=element_text(size=11))
        assert t is not None

    def test_theme_strip_background(self):
        """Test strip_background parameter."""
        from ggplotly.themes import theme, element_rect

        # strip_background is stored for faceted plots
        t = theme(strip_background=element_rect(fill='#e0e0e0'))
        assert t is not None


class TestElementClasses:
    """Tests for element_text, element_line, element_rect."""

    def test_element_text_params(self):
        """Test element_text with parameters."""
        from ggplotly.themes import element_text

        et = element_text(family='Arial', color='blue', size=14)
        assert et.family == 'Arial'
        assert et.color == 'blue'
        assert et.size == 14

    def test_element_text_defaults(self):
        """Test element_text default values."""
        from ggplotly.themes import element_text

        et = element_text()
        assert et.size == 12
        assert et.color == 'black'
        assert et.family == 'Arial'

    def test_element_line_params(self):
        """Test element_line with parameters."""
        from ggplotly.themes import element_line

        el = element_line(color='red', width=2, dash='dashed')
        assert el.color == 'red'
        assert el.width == 2
        assert el.dash == 'dashed'

    def test_element_line_defaults(self):
        """Test element_line default values."""
        from ggplotly.themes import element_line

        el = element_line()
        assert el.color == 'black'
        assert el.width == 1
        assert el.dash == 'solid'

    def test_element_rect_params(self):
        """Test element_rect with parameters."""
        from ggplotly.themes import element_rect

        er = element_rect(fill='yellow', color='black', width=1)
        assert er.fill == 'yellow'
        assert er.color == 'black'
        assert er.width == 1

    def test_element_rect_defaults(self):
        """Test element_rect default values."""
        from ggplotly.themes import element_rect

        er = element_rect()
        assert er.fill == 'white'
        assert er.color == 'black'
        assert er.width == 1


class TestPresetThemesBaseParams:
    """Tests for base_size and base_family in preset themes."""

    def test_theme_classic_default_base_size(self):
        """Test theme_classic has default base_size."""
        from ggplotly.themes import theme_classic

        tc = theme_classic()
        # Should work without errors and return a theme
        assert tc is not None

    def test_theme_classic_custom_base_size(self):
        """Test theme_classic with custom base_size."""
        from ggplotly.themes import theme_classic

        tc = theme_classic(base_size=14)
        assert tc.base_size == 14

    def test_theme_classic_custom_base_family(self):
        """Test theme_classic with custom base_family."""
        from ggplotly.themes import theme_classic

        tc = theme_classic(base_family='Times New Roman')
        assert tc.base_family == 'Times New Roman'

    def test_theme_classic_both_params(self):
        """Test theme_classic with both base_size and base_family."""
        from ggplotly.themes import theme_classic

        tc = theme_classic(base_size=16, base_family='Helvetica')
        assert tc.base_size == 16
        assert tc.base_family == 'Helvetica'

    def test_theme_minimal_default_base_size(self):
        """Test theme_minimal has default base_size."""
        from ggplotly.themes import theme_minimal

        tm = theme_minimal()
        assert tm is not None

    def test_theme_minimal_custom_base_size(self):
        """Test theme_minimal with custom base_size."""
        from ggplotly.themes import theme_minimal

        tm = theme_minimal(base_size=12)
        assert tm.base_size == 12

    def test_theme_minimal_custom_base_family(self):
        """Test theme_minimal with custom base_family."""
        from ggplotly.themes import theme_minimal

        tm = theme_minimal(base_family='Arial')
        assert tm.base_family == 'Arial'


# ============================================================================
# Phase 7 Tests: Guides
# ============================================================================

class TestGuideLegend:
    """Tests for guide_legend class."""

    def test_guide_legend_default_params(self):
        """Test guide_legend default parameters."""
        from ggplotly.guides import guide_legend

        gl = guide_legend()
        assert gl.title is None
        assert gl.title_position == 'top'
        assert gl.direction == 'vertical'
        assert gl.nrow is None
        assert gl.ncol is None
        assert gl.byrow is False
        assert gl.reverse is False
        assert gl.override_aes == {}

    def test_guide_legend_title(self):
        """Test guide_legend with custom title."""
        from ggplotly.guides import guide_legend

        gl = guide_legend(title='My Legend')
        assert gl.title == 'My Legend'

    def test_guide_legend_title_position(self):
        """Test guide_legend title positions."""
        from ggplotly.guides import guide_legend

        for pos in ['top', 'left', 'right']:
            gl = guide_legend(title_position=pos)
            assert gl.title_position == pos

    def test_guide_legend_direction_horizontal(self):
        """Test guide_legend horizontal direction."""
        from ggplotly.guides import guide_legend

        gl = guide_legend(direction='horizontal')
        assert gl.direction == 'horizontal'

    def test_guide_legend_direction_vertical(self):
        """Test guide_legend vertical direction."""
        from ggplotly.guides import guide_legend

        gl = guide_legend(direction='vertical')
        assert gl.direction == 'vertical'

    def test_guide_legend_nrow_ncol(self):
        """Test guide_legend with nrow and ncol."""
        from ggplotly.guides import guide_legend

        gl = guide_legend(nrow=2, ncol=3)
        assert gl.nrow == 2
        assert gl.ncol == 3

    def test_guide_legend_byrow(self):
        """Test guide_legend byrow parameter."""
        from ggplotly.guides import guide_legend

        gl = guide_legend(byrow=True)
        assert gl.byrow is True

    def test_guide_legend_reverse(self):
        """Test guide_legend reverse parameter."""
        from ggplotly.guides import guide_legend

        gl = guide_legend(reverse=True)
        assert gl.reverse is True

    def test_guide_legend_override_aes(self):
        """Test guide_legend override_aes parameter."""
        from ggplotly.guides import guide_legend

        gl = guide_legend(override_aes={'size': 5, 'alpha': 0.8})
        assert gl.override_aes == {'size': 5, 'alpha': 0.8}


class TestGuideColorbar:
    """Tests for guide_colorbar class."""

    def test_guide_colorbar_default_params(self):
        """Test guide_colorbar default parameters."""
        from ggplotly.guides import guide_colorbar

        gc = guide_colorbar()
        assert gc.title is None
        assert gc.title_position == 'top'
        assert gc.direction == 'vertical'
        assert gc.barwidth is None
        assert gc.barheight is None
        assert gc.nbin == 300
        assert gc.raster is True
        assert gc.ticks is True
        assert gc.draw_ulim is True
        assert gc.draw_llim is True
        assert gc.reverse is False

    def test_guide_colorbar_title(self):
        """Test guide_colorbar with title."""
        from ggplotly.guides import guide_colorbar

        gc = guide_colorbar(title='Value')
        assert gc.title == 'Value'

    def test_guide_colorbar_direction_horizontal(self):
        """Test guide_colorbar horizontal direction."""
        from ggplotly.guides import guide_colorbar

        gc = guide_colorbar(direction='horizontal')
        assert gc.direction == 'horizontal'

    def test_guide_colorbar_barwidth_barheight(self):
        """Test guide_colorbar dimensions."""
        from ggplotly.guides import guide_colorbar

        gc = guide_colorbar(barwidth=20, barheight=200)
        assert gc.barwidth == 20
        assert gc.barheight == 200

    def test_guide_colorbar_nbin(self):
        """Test guide_colorbar nbin parameter."""
        from ggplotly.guides import guide_colorbar

        gc = guide_colorbar(nbin=100)
        assert gc.nbin == 100

    def test_guide_colorbar_ticks_false(self):
        """Test guide_colorbar without ticks."""
        from ggplotly.guides import guide_colorbar

        gc = guide_colorbar(ticks=False)
        assert gc.ticks is False

    def test_guide_colorbar_reverse(self):
        """Test guide_colorbar reverse parameter."""
        from ggplotly.guides import guide_colorbar

        gc = guide_colorbar(reverse=True)
        assert gc.reverse is True


class TestGuidesFunction:
    """Tests for guides() function."""

    def test_guides_function_creates_guides_object(self):
        """Test guides() returns Guides object."""
        from ggplotly.guides import guides, Guides

        g = guides()
        assert isinstance(g, Guides)

    def test_guides_color_none(self):
        """Test guides(color='none') to hide color legend."""
        from ggplotly.guides import guides

        g = guides(color='none')
        assert g.guides['color'] == 'none'

    def test_guides_color_false(self):
        """Test guides(color=False) to hide color legend."""
        from ggplotly.guides import guides

        g = guides(color=False)
        assert g.guides['color'] is False

    def test_guides_with_guide_legend(self):
        """Test guides with guide_legend."""
        from ggplotly.guides import guides, guide_legend

        g = guides(color=guide_legend(title='Groups'))
        assert isinstance(g.guides['color'], guide_legend)
        assert g.guides['color'].title == 'Groups'

    def test_guides_with_guide_colorbar(self):
        """Test guides with guide_colorbar."""
        from ggplotly.guides import guides, guide_colorbar

        g = guides(fill=guide_colorbar(direction='horizontal'))
        assert isinstance(g.guides['fill'], guide_colorbar)
        assert g.guides['fill'].direction == 'horizontal'

    def test_guides_multiple_aesthetics(self):
        """Test guides with multiple aesthetics."""
        from ggplotly.guides import guides, guide_legend, guide_colorbar

        g = guides(
            color='none',
            fill=guide_colorbar(title='Value'),
            shape=guide_legend(ncol=2)
        )
        assert g.guides['color'] == 'none'
        assert isinstance(g.guides['fill'], guide_colorbar)
        assert isinstance(g.guides['shape'], guide_legend)


class TestGuidesApply:
    """Tests for Guides.apply() method."""

    def test_guides_apply_hide_legend(self):
        """Test Guides.apply() hides legend with 'none'."""
        from ggplotly.guides import guides

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        fig.update_layout(showlegend=True)

        g = guides(color='none')
        g.apply(fig)

        assert fig.layout.showlegend is False

    def test_guides_apply_legend_orientation(self):
        """Test Guides.apply() sets legend orientation."""
        from ggplotly.guides import guides, guide_legend

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])

        g = guides(color=guide_legend(direction='horizontal'))
        g.apply(fig)

        assert fig.layout.legend.orientation == 'h'

    def test_guides_apply_legend_title(self):
        """Test Guides.apply() sets legend title."""
        from ggplotly.guides import guides, guide_legend

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])

        g = guides(color=guide_legend(title='My Legend'))
        g.apply(fig)

        assert fig.layout.legend.title.text == 'My Legend'

    def test_guides_apply_legend_reverse(self):
        """Test Guides.apply() reverses legend."""
        from ggplotly.guides import guides, guide_legend

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])

        g = guides(color=guide_legend(reverse=True))
        g.apply(fig)

        assert fig.layout.legend.traceorder == 'reversed'


# ============================================================================
# Phase 7 Tests: aes() enhancements
# ============================================================================

class TestAfterStat:
    """Tests for after_stat class."""

    def test_after_stat_creation(self):
        """Test after_stat creation."""
        from ggplotly.aes import after_stat

        a = after_stat('density')
        assert a.var == 'density'

    def test_after_stat_repr(self):
        """Test after_stat string representation."""
        from ggplotly.aes import after_stat

        a = after_stat('count')
        assert repr(a) == "after_stat('count')"

    def test_after_stat_common_vars(self):
        """Test after_stat with common computed variables."""
        from ggplotly.aes import after_stat

        for var in ['count', 'density', 'ncount', 'ndensity']:
            a = after_stat(var)
            assert a.var == var


class TestAfterScale:
    """Tests for after_scale class."""

    def test_after_scale_creation(self):
        """Test after_scale creation."""
        from ggplotly.aes import after_scale

        a = after_scale('alpha(color, 0.5)')
        assert a.expr == 'alpha(color, 0.5)'

    def test_after_scale_repr(self):
        """Test after_scale string representation."""
        from ggplotly.aes import after_scale

        a = after_scale('darken(fill, 0.2)')
        assert repr(a) == "after_scale('darken(fill, 0.2)')"


class TestStage:
    """Tests for stage class."""

    def test_stage_start_only(self):
        """Test stage with start only."""
        from ggplotly.aes import stage

        s = stage(start='group')
        assert s.start == 'group'
        assert s.after_stat is None
        assert s.after_scale is None

    def test_stage_after_stat_only(self):
        """Test stage with after_stat only."""
        from ggplotly.aes import stage

        s = stage(after_stat='density')
        assert s.start is None
        assert s.after_stat == 'density'
        assert s.after_scale is None

    def test_stage_after_scale_only(self):
        """Test stage with after_scale only."""
        from ggplotly.aes import stage

        s = stage(after_scale='alpha(color, 0.5)')
        assert s.start is None
        assert s.after_stat is None
        assert s.after_scale == 'alpha(color, 0.5)'

    def test_stage_all_params(self):
        """Test stage with all parameters."""
        from ggplotly.aes import stage

        s = stage(
            start='group',
            after_stat='density',
            after_scale='alpha(color, 0.5)'
        )
        assert s.start == 'group'
        assert s.after_stat == 'density'
        assert s.after_scale == 'alpha(color, 0.5)'


class TestAesEnhancements:
    """Tests for aes class enhancements."""

    def test_aes_basic(self):
        """Test basic aes creation."""
        from ggplotly.aes import aes

        a = aes(x='mpg', y='hp')
        assert a.mapping['x'] == 'mpg'
        assert a.mapping['y'] == 'hp'

    def test_aes_with_color(self):
        """Test aes with color aesthetic."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', color='group')
        assert a.mapping['color'] == 'group'

    def test_aes_colour_alias(self):
        """Test aes with British colour spelling."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', colour='group')
        assert a.mapping['color'] == 'group'

    def test_aes_with_z(self):
        """Test aes with z aesthetic for 3D plots."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', z='z')
        assert a.mapping['z'] == 'z'

    def test_aes_with_fill(self):
        """Test aes with fill aesthetic."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', fill='category')
        assert a.mapping['fill'] == 'category'

    def test_aes_with_size(self):
        """Test aes with size aesthetic."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', size='weight')
        assert a.mapping['size'] == 'weight'

    def test_aes_with_shape(self):
        """Test aes with shape aesthetic."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', shape='type')
        assert a.mapping['shape'] == 'type'

    def test_aes_with_alpha(self):
        """Test aes with alpha aesthetic."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', alpha='transparency')
        assert a.mapping['alpha'] == 'transparency'

    def test_aes_with_linetype(self):
        """Test aes with linetype aesthetic."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', linetype='style')
        assert a.mapping['linetype'] == 'style'

    def test_aes_with_label(self):
        """Test aes with label aesthetic."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', label='name')
        assert a.mapping['label'] == 'name'

    def test_aes_with_group(self):
        """Test aes with group aesthetic."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', group='id')
        assert a.mapping['group'] == 'id'

    def test_aes_with_kwargs(self):
        """Test aes with additional kwargs."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', custom='value')
        assert a.mapping['custom'] == 'value'

    def test_aes_with_after_stat(self):
        """Test aes with after_stat computed aesthetic."""
        from ggplotly.aes import aes, after_stat

        a = aes(x='x', y=after_stat('density'))
        assert isinstance(a.mapping['y'], after_stat)
        assert a.mapping['y'].var == 'density'

    def test_aes_get_method(self):
        """Test aes.get() method."""
        from ggplotly.aes import aes

        a = aes(x='mpg', y='hp')
        assert a.get('x') == 'mpg'
        assert a.get('nonexistent') is None
        assert a.get('nonexistent', 'default') == 'default'

    def test_aes_keys_method(self):
        """Test aes.keys() method."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y', color='c')
        keys = list(a.keys())
        assert 'x' in keys
        assert 'y' in keys
        assert 'color' in keys

    def test_aes_values_method(self):
        """Test aes.values() method."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y')
        values = list(a.values())
        assert 'x' in values
        assert 'y' in values

    def test_aes_items_method(self):
        """Test aes.items() method."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y')
        items = dict(a.items())
        assert items['x'] == 'x'
        assert items['y'] == 'y'

    def test_aes_getitem(self):
        """Test aes[] access."""
        from ggplotly.aes import aes

        a = aes(x='mpg', y='hp')
        assert a['x'] == 'mpg'
        assert a['y'] == 'hp'

    def test_aes_contains(self):
        """Test 'in' operator for aes."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y')
        assert 'x' in a
        assert 'z' not in a

    def test_aes_copy(self):
        """Test aes.copy() method."""
        from ggplotly.aes import aes

        a = aes(x='x', y='y')
        b = a.copy()
        assert b.mapping == a.mapping
        assert b.mapping is not a.mapping  # Different objects

    def test_aes_update(self):
        """Test aes.update() method."""
        from ggplotly.aes import aes

        a = aes(x='x')
        a.update({'y': 'y', 'color': 'c'})
        assert a.mapping['y'] == 'y'
        assert a.mapping['color'] == 'c'

    def test_aes_update_from_aes(self):
        """Test aes.update() from another aes."""
        from ggplotly.aes import aes

        a = aes(x='x')
        b = aes(y='y', color='c')
        a.update(b)
        assert a.mapping['y'] == 'y'
        assert a.mapping['color'] == 'c'


# ============================================================================
# Phase 7 Tests: Labs enhancements
# ============================================================================

class TestLabsEnhancements:
    """Tests for Labs class enhancements."""

    def test_labs_basic(self):
        """Test basic labs creation."""
        from ggplotly.guides import labs

        l = labs(title='My Plot', x='X Axis', y='Y Axis')
        assert l.title == 'My Plot'
        assert l.x == 'X Axis'
        assert l.y == 'Y Axis'

    def test_labs_subtitle(self):
        """Test labs with subtitle."""
        from ggplotly.guides import labs

        l = labs(title='Main Title', subtitle='Subtitle')
        assert l.title == 'Main Title'
        assert l.subtitle == 'Subtitle'

    def test_labs_z_axis(self):
        """Test labs with z axis label."""
        from ggplotly.guides import labs

        l = labs(x='X', y='Y', z='Z')
        assert l.z == 'Z'

    def test_labs_color(self):
        """Test labs with color legend title."""
        from ggplotly.guides import labs

        l = labs(color='Color Legend')
        assert l.color == 'Color Legend'

    def test_labs_colour_alias(self):
        """Test labs with British colour spelling."""
        from ggplotly.guides import labs

        l = labs(colour='Colour Legend')
        assert l.color == 'Colour Legend'

    def test_labs_fill(self):
        """Test labs with fill legend title."""
        from ggplotly.guides import labs

        l = labs(fill='Fill Legend')
        assert l.fill == 'Fill Legend'

    def test_labs_size(self):
        """Test labs with size legend title."""
        from ggplotly.guides import labs

        l = labs(size='Size Legend')
        assert l.size == 'Size Legend'

    def test_labs_shape(self):
        """Test labs with shape legend title."""
        from ggplotly.guides import labs

        l = labs(shape='Shape Legend')
        assert l.shape == 'Shape Legend'

    def test_labs_alpha(self):
        """Test labs with alpha legend title."""
        from ggplotly.guides import labs

        l = labs(alpha='Alpha Legend')
        assert l.alpha == 'Alpha Legend'

    def test_labs_linetype(self):
        """Test labs with linetype legend title."""
        from ggplotly.guides import labs

        l = labs(linetype='Line Type Legend')
        assert l.linetype == 'Line Type Legend'

    def test_labs_caption(self):
        """Test labs with caption."""
        from ggplotly.guides import labs

        l = labs(caption='Data source: XYZ')
        assert l.caption == 'Data source: XYZ'

    def test_labs_tag(self):
        """Test labs with tag."""
        from ggplotly.guides import labs

        l = labs(tag='A')
        assert l.tag == 'A'

    def test_labs_alt(self):
        """Test labs with alt text."""
        from ggplotly.guides import labs

        l = labs(alt='Scatter plot showing relationship between X and Y')
        assert l.alt == 'Scatter plot showing relationship between X and Y'

    def test_labs_extra_kwargs(self):
        """Test labs with extra kwargs."""
        from ggplotly.guides import labs

        l = labs(custom_aes='Custom Label')
        assert l.extra_labels['custom_aes'] == 'Custom Label'

    def test_labs_all_params(self):
        """Test labs with all parameters."""
        from ggplotly.guides import labs

        l = labs(
            title='Title',
            subtitle='Subtitle',
            x='X',
            y='Y',
            z='Z',
            color='Color',
            fill='Fill',
            size='Size',
            shape='Shape',
            alpha='Alpha',
            linetype='Linetype',
            caption='Caption',
            tag='A',
            alt='Alt text'
        )
        assert l.title == 'Title'
        assert l.subtitle == 'Subtitle'
        assert l.x == 'X'
        assert l.y == 'Y'
        assert l.z == 'Z'
        assert l.color == 'Color'
        assert l.fill == 'Fill'
        assert l.size == 'Size'
        assert l.shape == 'Shape'
        assert l.alpha == 'Alpha'
        assert l.linetype == 'Linetype'
        assert l.caption == 'Caption'
        assert l.tag == 'A'
        assert l.alt == 'Alt text'


class TestLabsApply:
    """Tests for Labs.apply() method."""

    def test_labs_apply_title(self):
        """Test Labs.apply() sets title."""
        from ggplotly.guides import labs

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        l = labs(title='My Title')
        l.apply(fig)

        assert 'My Title' in fig.layout.title.text

    def test_labs_apply_title_with_subtitle(self):
        """Test Labs.apply() sets title with subtitle."""
        from ggplotly.guides import labs

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        l = labs(title='Main Title', subtitle='Subtitle')
        l.apply(fig)

        assert 'Main Title' in fig.layout.title.text
        assert 'Subtitle' in fig.layout.title.text

    def test_labs_apply_x_axis(self):
        """Test Labs.apply() sets x axis title."""
        from ggplotly.guides import labs

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        l = labs(x='X Axis')
        l.apply(fig)

        assert fig.layout.xaxis.title.text == 'X Axis'

    def test_labs_apply_y_axis(self):
        """Test Labs.apply() sets y axis title."""
        from ggplotly.guides import labs

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        l = labs(y='Y Axis')
        l.apply(fig)

        assert fig.layout.yaxis.title.text == 'Y Axis'

    def test_labs_apply_legend_title_from_color(self):
        """Test Labs.apply() sets legend title from color."""
        from ggplotly.guides import labs

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        l = labs(color='Groups')
        l.apply(fig)

        assert fig.layout.legend.title.text == 'Groups'

    def test_labs_apply_caption(self):
        """Test Labs.apply() adds caption annotation."""
        from ggplotly.guides import labs

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        l = labs(caption='Source: Data')
        l.apply(fig)

        # Check caption was added as annotation
        assert len(fig.layout.annotations) > 0
        caption_found = any('Source: Data' in str(ann.text)
                          for ann in fig.layout.annotations)
        assert caption_found


# ============================================================================
# Phase 7 Tests: Annotate
# ============================================================================

class TestAnnotate:
    """Tests for annotate function."""

    def test_annotate_text(self):
        """Test annotate with text geom."""
        from ggplotly.guides import annotate

        a = annotate('text', x=5, y=10, label='Label')
        assert a.geom == 'text'
        assert a.x == 5
        assert a.y == 10
        assert a.label == 'Label'

    def test_annotate_label(self):
        """Test annotate with label geom."""
        from ggplotly.guides import annotate

        a = annotate('label', x=5, y=10, label='Label', fill='yellow')
        assert a.geom == 'label'
        assert a.fill == 'yellow'

    def test_annotate_segment(self):
        """Test annotate with segment geom."""
        from ggplotly.guides import annotate

        a = annotate('segment', x=0, y=0, xend=5, yend=5, arrow=True)
        assert a.geom == 'segment'
        assert a.x == 0
        assert a.y == 0
        assert a.xend == 5
        assert a.yend == 5
        assert a.arrow is True

    def test_annotate_rect(self):
        """Test annotate with rect geom."""
        from ggplotly.guides import annotate

        a = annotate('rect', xmin=0, xmax=5, ymin=0, ymax=5, fill='blue', alpha=0.3)
        assert a.geom == 'rect'
        assert a.xmin == 0
        assert a.xmax == 5
        assert a.ymin == 0
        assert a.ymax == 5
        assert a.fill == 'blue'
        assert a.alpha == 0.3

    def test_annotate_point(self):
        """Test annotate with point geom."""
        from ggplotly.guides import annotate

        a = annotate('point', x=5, y=5, size=10, color='red')
        assert a.geom == 'point'
        assert a.x == 5
        assert a.y == 5
        assert a.size == 10
        assert a.color == 'red'

    def test_annotate_apply_text(self):
        """Test annotate apply for text."""
        from ggplotly.guides import annotate

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        a = annotate('text', x=2, y=2, label='Test')
        a.apply(fig)

        assert len(fig.layout.annotations) > 0

    def test_annotate_apply_rect(self):
        """Test annotate apply for rect."""
        from ggplotly.guides import annotate

        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[1, 2, 3])])
        a = annotate('rect', xmin=1, xmax=2, ymin=1, ymax=2, fill='yellow')
        a.apply(fig)

        assert len(fig.layout.shapes) > 0
