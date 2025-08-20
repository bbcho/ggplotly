# GGPLOTLY Testing Suite

This directory contains comprehensive tests for the ggplotly library, covering all major components and functionality.

## Test Coverage

The test suite covers the following areas:

### 1. **Geometries (Geoms)** - `test_geoms.py`
- **Point plots**: Basic points, colored points, sized points
- **Line plots**: Basic lines, grouped lines
- **Bar plots**: Basic bars, filled bars
- **Histograms**: Basic histograms, custom bins
- **Boxplots**: Basic boxplots
- **Area plots**: Basic areas, filled areas
- **Density plots**: Basic density estimation
- **Violin plots**: Basic violin plots
- **Smooth plots**: Basic smoothing, method specification
- **Text plots**: Basic text annotations
- **Error bars**: Basic error bar plots
- **Tile plots**: Basic tile/heatmap plots
- **Ribbon plots**: Basic ribbon plots
- **Step plots**: Basic step plots
- **Segment plots**: Basic segment plots
- **Reference lines**: Horizontal and vertical lines
- **Combinations**: Multiple geometries on same plot

### 2. **Scales** - `test_scales.py`
- **Continuous scales**: X and Y axis limits, breaks
- **Log scales**: X and Y log10 transformations
- **Color scales**: Manual colors, color brewer, gradients
- **Fill scales**: Manual fills, fill gradients
- **Size scales**: Size range specifications
- **Combinations**: Multiple scales on same plot
- **Edge cases**: Invalid limits, breaks, palettes

### 3. **Themes and Coordinates** - `test_themes_and_coords.py`
- **Built-in themes**: Default, minimal, dark, classic, BBC, NYTimes
- **Custom themes**: Template-based custom themes
- **Coordinate systems**: Cartesian, flipped, polar
- **Theme elements**: Text, line, rectangle styling
- **Combinations**: Themes with coordinates, scales, faceting

### 4. **Faceting, Stats, and Utilities** - `test_facets_stats_utils.py`
- **Faceting**: Wrap and grid faceting with various parameters
- **Statistical transformations**: Binning, counting, density, ECDF, smoothing
- **Utility functions**: Titles, labels, saving, sizing, positions
- **Combinations**: Faceting with stats, themes, scales

### 5. **Error Handling** - `test_error_handling.py`
- **Invalid data**: None data, empty dataframes, missing columns
- **Invalid components**: Wrong component types, None components
- **Invalid parameters**: Invalid colors, sizes, limits, methods
- **Edge cases**: Single rows, single columns, duplicate columns
- **Large data**: Memory usage, performance with large datasets
- **Missing values**: NaN, infinite values

### 6. **Integration Tests** - `test_integration.py`
- **Complex plot combinations**: Multiple geoms, scales, themes
- **Real-world scenarios**: Time series, faceted plots, statistical plots
- **Performance testing**: Large datasets, memory usage
- **Advanced features**: Custom themes, coordinate systems, positioning
- **Plot saving**: Export functionality verification

## Running Tests

### Prerequisites

Install testing dependencies:
```bash
pip install -r pytest/requirements-test.txt
```

### Basic Test Execution

Run all tests:
```bash
python -m pytest pytest/
```

Run with verbose output:
```bash
python -m pytest pytest/ -v
```

### Using the Test Runner Script

The `run_tests.py` script provides convenient options:

```bash
# Check test environment
python pytest/run_tests.py --check

# List available test files
python pytest/run_tests.py --list

# Run all tests with coverage
python pytest/run_tests.py --coverage --verbose

# Run specific test file
python pytest/run_tests.py --file pytest/test_geoms.py --verbose

# Run specific test class
python pytest/run_tests.py --file pytest/test_geoms.py --class TestGeoms --verbose

# Generate HTML report
python pytest/run_tests.py --html-report --coverage

# Run tests in parallel
python pytest/run_tests.py --parallel --verbose
```

### Running Specific Test Categories

Run only geometry tests:
```bash
python -m pytest pytest/test_geoms.py -v
```

Run only scale tests:
```bash
python -m pytest pytest/test_scales.py -v
```

Run only theme and coordinate tests:
```bash
python -m pytest pytest/test_themes_and_coords.py -v
```

Run only faceting and utility tests:
```bash
python -m pytest pytest/test_facets_stats_utils.py -v
```

Run only error handling tests:
```bash
python -m pytest pytest/test_error_handling.py -v
```

### Coverage Reports

Generate coverage report:
```bash
python -m pytest pytest/ --cov=ggplotly --cov-report=term-missing
```

Generate HTML coverage report:
```bash
python -m pytest pytest/ --cov=ggplotly --cov-report=html
```

## Test Structure

### Test Classes

Each test file contains a test class with methods for different functionality:

- **`TestGeoms`**: Tests for all geometry types
- **`TestScales`**: Tests for all scale transformations
- **`TestThemesAndCoordinates`**: Tests for themes and coordinate systems
- **`TestFacetsStatsUtils`**: Tests for faceting, stats, and utilities
- **`TestErrorHandling`**: Tests for error conditions and edge cases
- **`TestIntegration`**: Tests for complex plot combinations and real-world scenarios

### Test Methods

Each test method follows a consistent naming convention:
- `test_[component]_[functionality]`: Basic functionality tests
- `test_[component]_with_[parameter]`: Parameter-specific tests
- `test_[component]_edge_cases`: Edge case tests
- `test_[component]_combinations`: Combination tests

### Test Data

Tests use standardized test data provided by fixtures:
- **`sample_data`**: Basic 5-row dataset with various data types
- **`sample_data_large`**: 100-row dataset for performance testing
- **`sample_data_grid`**: Grid data for tile plots
- **`sample_data_error`**: Data with error bars
- **`sample_data_ribbon`**: Data for ribbon plots
- **`empty_dataframe`**: Empty dataframe for edge cases
- **`single_row_data`**: Single row data for edge cases
- **`single_column_data`**: Single column data for edge cases

## Adding New Tests

### Adding New Test Methods

1. **Follow naming convention**: `test_[component]_[functionality]`
2. **Use descriptive docstrings**: Explain what the test validates
3. **Use appropriate fixtures**: Leverage existing test data
4. **Test both success and failure cases**: Include edge cases
5. **Assert meaningful conditions**: Check actual functionality, not just that it runs

### Example Test Method

```python
def test_geom_new_feature(self):
    """Test new feature of geometry component."""
    p = ggplot(self.df, aes(x='x', y='y')) + geom_new_feature()
    fig = p.draw()
    
    # Assert the expected behavior
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1
    assert fig.data[0].type == 'expected_type'
```

### Adding New Test Files

1. **Create new file**: `test_[component].py`
2. **Import dependencies**: Import required modules and ggplotly
3. **Create test class**: Inherit from appropriate base class if needed
4. **Add test methods**: Implement comprehensive test coverage
5. **Update test runner**: Add to test discovery if needed

## Test Best Practices

### 1. **Isolation**
- Each test should be independent
- Use `setup_method()` for test data setup
- Avoid sharing state between tests

### 2. **Completeness**
- Test both valid and invalid inputs
- Test edge cases and boundary conditions
- Test combinations of components

### 3. **Readability**
- Use descriptive test names
- Add clear docstrings
- Use meaningful assertions

### 4. **Performance**
- Keep tests fast and focused
- Use appropriate data sizes
- Avoid unnecessary computations

### 5. **Maintenance**
- Update tests when functionality changes
- Remove obsolete tests
- Keep test data current

## Troubleshooting

### Common Issues

1. **Import errors**: Ensure ggplotly is in Python path
2. **Missing dependencies**: Install required packages
3. **Test failures**: Check test data and assertions
4. **Performance issues**: Reduce test data size

### Debug Mode

Run tests with debug output:
```bash
python -m pytest pytest/ -v -s --tb=long
```

### Test Discovery

Check which tests are discovered:
```bash
python -m pytest pytest/ --collect-only
```

## Continuous Integration

The test suite is designed to work with CI/CD systems:

- **GitHub Actions**: Use `pytest/` directory
- **Travis CI**: Configure to run pytest
- **Jenkins**: Execute test runner script
- **Local development**: Use test runner for convenience

## Contributing

When contributing to the test suite:

1. **Follow existing patterns**: Match style and structure
2. **Add comprehensive coverage**: Test new functionality thoroughly
3. **Update documentation**: Keep this README current
4. **Run tests locally**: Ensure all tests pass before submitting
5. **Add new fixtures**: Create reusable test data when needed

## Support

For questions about the testing suite:

1. **Check existing tests**: Look for similar examples
2. **Review test data**: Understand available fixtures
3. **Run test runner**: Use `--help` for options
4. **Check coverage**: Identify untested areas
5. **Review documentation**: Check this README and docstrings

