import pandas as pd

import pytest
from ggplotly import aes, geom_sankey, ggplot


class TestGeomSankey:
    """Tests for geom_sankey."""

    def test_basic_sankey(self):
        """Test basic Sankey diagram returns correct trace type and structure."""
        df = pd.DataFrame({
            'source': ['A', 'A', 'B', 'B'],
            'target': ['X', 'Y', 'X', 'Y'],
            'value': [10, 20, 15, 25]
        })

        plot = (ggplot(df, aes(source='source', target='target', value='value'))
                + geom_sankey())
        fig = plot.draw()

        # Verify trace type
        assert len(fig.data) == 1
        assert fig.data[0].type == 'sankey'

        # Verify link values are correctly passed
        assert list(fig.data[0].link.value) == [10, 20, 15, 25]

        # Verify number of links matches data rows
        assert len(fig.data[0].link.source) == 4
        assert len(fig.data[0].link.target) == 4

    def test_multi_stage_sankey(self):
        """Test multi-stage Sankey diagram has correct node and link count."""
        df = pd.DataFrame({
            'source': ['Budget', 'Budget', 'Sales', 'Sales', 'Marketing', 'Marketing'],
            'target': ['Sales', 'Marketing', 'Revenue', 'Costs', 'Revenue', 'Costs'],
            'value': [100, 50, 80, 20, 40, 10]
        })

        plot = (ggplot(df, aes(source='source', target='target', value='value'))
                + geom_sankey())
        fig = plot.draw()

        assert fig.data[0].type == 'sankey'

        # Should have 6 links
        assert len(fig.data[0].link.source) == 6

        # Should have 5 unique nodes: Budget, Sales, Marketing, Revenue, Costs
        assert len(fig.data[0].node.label) == 5

        # Verify flow values
        assert list(fig.data[0].link.value) == [100, 50, 80, 20, 40, 10]

    def test_custom_node_colors(self):
        """Test custom node colors are applied correctly."""
        df = pd.DataFrame({
            'source': ['A', 'A'],
            'target': ['X', 'Y'],
            'value': [10, 20]
        })

        plot = (ggplot(df, aes(source='source', target='target', value='value'))
                + geom_sankey(node_color=['red', 'blue', 'green']))
        fig = plot.draw()

        # Verify colors are assigned
        assert fig.data[0].node.color[0] == 'red'
        assert fig.data[0].node.color[1] == 'blue'
        assert fig.data[0].node.color[2] == 'green'

    def test_single_node_color(self):
        """Test single node color is applied to all nodes."""
        df = pd.DataFrame({
            'source': ['A', 'B'],
            'target': ['X', 'X'],
            'value': [10, 20]
        })

        plot = (ggplot(df, aes(source='source', target='target', value='value'))
                + geom_sankey(node_color='steelblue'))
        fig = plot.draw()

        # All nodes should have the same color
        assert all(c == 'steelblue' for c in fig.data[0].node.color)
        assert len(fig.data[0].node.color) == 3  # A, B, X

    def test_custom_parameters(self):
        """Test custom node padding and thickness parameters."""
        df = pd.DataFrame({
            'source': ['A', 'B'],
            'target': ['X', 'X'],
            'value': [10, 20]
        })

        plot = (ggplot(df, aes(source='source', target='target', value='value'))
                + geom_sankey(node_pad=30, node_thickness=40))
        fig = plot.draw()

        assert fig.data[0].node.pad == 30
        assert fig.data[0].node.thickness == 40

    def test_vertical_orientation(self):
        """Test vertical orientation is set correctly."""
        df = pd.DataFrame({
            'source': ['A', 'B'],
            'target': ['X', 'X'],
            'value': [10, 20]
        })

        plot = (ggplot(df, aes(source='source', target='target', value='value'))
                + geom_sankey(orientation='v'))
        fig = plot.draw()

        assert fig.data[0].orientation == 'v'

    def test_horizontal_orientation_default(self):
        """Test horizontal orientation is the default."""
        df = pd.DataFrame({
            'source': ['A', 'B'],
            'target': ['X', 'X'],
            'value': [10, 20]
        })

        plot = (ggplot(df, aes(source='source', target='target', value='value'))
                + geom_sankey())
        fig = plot.draw()

        assert fig.data[0].orientation == 'h'

    def test_link_indices_are_correct(self):
        """Test that source/target indices correctly reference nodes."""
        df = pd.DataFrame({
            'source': ['A', 'A', 'B'],
            'target': ['X', 'Y', 'X'],
            'value': [10, 20, 15]
        })

        plot = (ggplot(df, aes(source='source', target='target', value='value'))
                + geom_sankey())
        fig = plot.draw()

        # Get node labels
        labels = list(fig.data[0].node.label)
        source_indices = list(fig.data[0].link.source)
        target_indices = list(fig.data[0].link.target)

        # Verify each link connects correct nodes
        for i, (src_idx, tgt_idx, val) in enumerate(zip(source_indices, target_indices, [10, 20, 15])):
            expected_source = df.iloc[i]['source']
            expected_target = df.iloc[i]['target']
            assert labels[src_idx] == expected_source
            assert labels[tgt_idx] == expected_target

    def test_missing_aesthetics_raises(self):
        """Test that missing required aesthetics raises RequiredAestheticError."""
        from ggplotly.exceptions import RequiredAestheticError

        df = pd.DataFrame({
            'source': ['A', 'B'],
            'target': ['X', 'X'],
            'value': [10, 20]
        })

        # Missing value
        plot = (ggplot(df, aes(source='source', target='target'))
                + geom_sankey())
        with pytest.raises(RequiredAestheticError, match="value"):
            plot.draw()

        # Missing source
        plot2 = (ggplot(df, aes(target='target', value='value'))
                 + geom_sankey())
        with pytest.raises(RequiredAestheticError, match="source"):
            plot2.draw()

    def test_missing_column_raises(self):
        """Test that missing data column raises ValueError."""
        df = pd.DataFrame({
            'source': ['A', 'B'],
            'value': [10, 20]
        })

        plot = (ggplot(df, aes(source='source', target='nonexistent', value='value'))
                + geom_sankey())
        with pytest.raises(ValueError, match="not found"):
            plot.draw()

    def test_node_labels(self):
        """Test that node labels are extracted correctly from unique source/target values."""
        df = pd.DataFrame({
            'source': ['A', 'A', 'B'],
            'target': ['X', 'Y', 'X'],
            'value': [10, 20, 15]
        })

        plot = (ggplot(df, aes(source='source', target='target', value='value'))
                + geom_sankey())
        fig = plot.draw()

        # Should have 4 unique nodes: A, B, X, Y
        labels = list(fig.data[0].node.label)
        assert len(labels) == 4
        assert 'A' in labels
        assert 'B' in labels
        assert 'X' in labels
        assert 'Y' in labels

    def test_link_alpha(self):
        """Test that link alpha/transparency is applied."""
        df = pd.DataFrame({
            'source': ['A', 'A'],
            'target': ['X', 'Y'],
            'value': [10, 20]
        })

        plot = (ggplot(df, aes(source='source', target='target', value='value'))
                + geom_sankey(link_alpha=0.8))
        fig = plot.draw()

        # Link colors should contain rgba with the specified alpha
        for color in fig.data[0].link.color:
            assert 'rgba' in color or color.startswith('#')
