# geoms/geom_range.py

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
from .geom_base import Geom


class geom_range(Geom):
    """
    Geom for drawing 5-year range plots with historical context.

    Shows historical min/max as a ribbon, historical average as a dotted line,
    prior year as a blue line, and current year as a red line. The historical
    statistics (min, max, avg) are calculated from the 5 years prior to the
    current year (excluding current year).

    Parameters:
        years (int): Number of historical years to include in range calculation.
            Default is 5.
        freq (str, optional): Pandas frequency string for resampling. Examples:
            - 'D': Daily
            - 'W': Weekly (Sunday end)
            - 'W-Fri': Weekly ending Friday
            - 'ME': Month end
            - 'MS': Month start
            - 'QE': Quarter end
            - '2W': Bi-weekly
            - None: Auto-detect based on data
        current_year (int, optional): Year to treat as "current". Default is
            the max year in the data.
        show_years (list, optional): Additional specific years to display as
            separate lines. Each will get a unique color.
        ribbon_color (str): Color for the historical range ribbon. Default is 'gray'.
        ribbon_alpha (float): Transparency for ribbon. Default is 0.3.
        avg_color (str): Color for average line. Default is 'black'.
        avg_linetype (str): Line style for average. Default is 'dot'.
        prior_color (str): Color for prior year line. Default is 'blue'.
        current_color (str): Color for current year line. Default is 'red'.
        show_legend (bool): Whether to show legend. Default is True.

    Aesthetics:
        - x: Date column (must be datetime or date type)
        - y: Value column

    Examples:
        # Basic 5-year range plot
        ggplot(df, aes(x='date', y='value')) + geom_range()

        # With weekly frequency ending Friday
        ggplot(df, aes(x='date', y='value')) + geom_range(freq='W-Fri')

        # Show specific additional years
        ggplot(df, aes(x='date', y='value')) + geom_range(show_years=[2019, 2020])

        # Custom colors
        ggplot(df, aes(x='date', y='value')) + geom_range(
            current_color='green',
            prior_color='orange'
        )
    """

    __name__ = "geom_range"

    def __init__(self, data=None, mapping=None, **params):
        """
        Initialize the range geom.

        Parameters:
            data (DataFrame, optional): Data for this geom.
            mapping (aes, optional): Aesthetic mappings.
            **params: Additional parameters (years, freq, colors, etc.).
        """
        super().__init__(data, mapping, **params)
        self.years = params.get('years', 5)
        self.freq = params.get('freq', None)
        self.current_year = params.get('current_year', None)
        self.show_years = params.get('show_years', None)
        self.ribbon_color = params.get('ribbon_color', 'gray')
        self.ribbon_alpha = params.get('ribbon_alpha', 0.3)
        self.avg_color = params.get('avg_color', 'black')
        self.avg_linetype = params.get('avg_linetype', 'dot')
        self.prior_color = params.get('prior_color', 'blue')
        self.current_color = params.get('current_color', 'red')
        self.show_legend = params.get('show_legend', True)

    def _detect_frequency(self, dates):
        """Auto-detect the frequency from index freq attribute or row differences."""
        # First, try to get frequency from DatetimeIndex
        if isinstance(dates, pd.DatetimeIndex):
            if dates.freq is not None:
                return dates.freq.freqstr
            # Try to infer frequency
            inferred = pd.infer_freq(dates)
            if inferred:
                return inferred

        # Convert to DatetimeIndex if needed and try to infer
        if not isinstance(dates, pd.DatetimeIndex):
            try:
                dt_index = pd.DatetimeIndex(dates)
                inferred = pd.infer_freq(dt_index)
                if inferred:
                    return inferred
            except (ValueError, TypeError):
                pass

        # Fall back to median difference calculation
        if len(dates) < 2:
            return 'D'

        sorted_dates = pd.to_datetime(dates).sort_values()
        diffs = sorted_dates.diff().dropna()
        median_diff = diffs.median().days

        if median_diff <= 1:
            return 'D'
        elif median_diff <= 8:
            return 'W'
        elif median_diff <= 35:
            return 'ME'
        else:
            return 'QE'

    def _normalize_freq(self, freq):
        """Normalize frequency string to pandas format."""
        if freq is None:
            return None
        freq_map = {
            'daily': 'D', 'd': 'D',
            'weekly': 'W', 'w': 'W',
            'monthly': 'ME', 'm': 'ME', 'M': 'ME',
            'quarterly': 'QE', 'q': 'QE', 'Q': 'QE',
        }
        return freq_map.get(freq, freq)

    def _is_weekly_or_finer(self, freq):
        """Check if frequency is weekly or finer (needs week-based alignment)."""
        if freq is None:
            return False
        freq_upper = freq.upper()
        # Weekly frequencies: W, W-MON, W-FRI, etc.
        if freq_upper.startswith('W'):
            return True
        # Daily or sub-daily
        if freq_upper in ['D', 'B', 'H', 'T', 'MIN', 'S']:
            return True
        # Bi-weekly or other multiplied weekly
        if 'W' in freq_upper and any(c.isdigit() for c in freq):
            return True
        return False

    def _resample_year(self, year_df, x_col, y_col, freq, reference_year):
        """Resample a single year's data and align dates to reference year."""
        if len(year_df) == 0:
            return pd.DataFrame()

        # Set date as index for resampling
        temp = year_df[[x_col, y_col]].copy()
        temp = temp.set_index(x_col)

        # Resample and aggregate with mean
        resampled = temp.resample(freq).mean().dropna()

        if len(resampled) == 0:
            return pd.DataFrame()

        resampled = resampled.reset_index()

        # For weekly or finer frequencies, align by week number
        # For monthly or coarser, align by shifting year
        if self._is_weekly_or_finer(freq):
            # Use week of year for alignment (1-52)
            resampled['_period'] = resampled[x_col].dt.isocalendar().week
            resampled['_month'] = resampled[x_col].dt.month
            # Exclude week 53, and week 52 in January (belongs to prev year)
            resampled = resampled[
                (resampled['_period'] <= 52) &
                ~((resampled['_period'] == 52) & (resampled['_month'] == 1))
            ]
            resampled = resampled.rename(columns={y_col: '_value'})
            return resampled[['_period', '_value']].sort_values('_period')
        else:
            # Monthly or coarser - shift to reference year
            def shift_to_reference_year(d):
                """Shift date to reference year, handling leap year edge cases."""
                try:
                    return d.replace(year=reference_year)
                except ValueError:
                    # Handle Feb 29 -> Feb 28 for non-leap years
                    if d.month == 2 and d.day == 29:
                        return d.replace(year=reference_year, day=28)
                    raise

            resampled['_date'] = resampled[x_col].apply(shift_to_reference_year)
            resampled = resampled.rename(columns={y_col: '_value'})
            return resampled[['_date', '_value']].sort_values('_date')

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw range plot on the figure with historical context.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = data if data is not None else self.data

        x_col = self.mapping.get('x')
        y_col = self.mapping.get('y')

        # Handle datetime in index
        df = data.copy()
        datetime_in_index = False

        if isinstance(df.index, pd.DatetimeIndex):
            datetime_in_index = True
            # Store original index freq for detection
            original_index = df.index
            # Reset index to make datetime a column
            if x_col is None:
                x_col = '_datetime_index'
                df = df.reset_index(names=x_col)
            else:
                df = df.reset_index(drop=True)

        if x_col is None or y_col is None:
            raise ValueError("geom_range requires both 'x' (date) and 'y' (value) aesthetics")

        # Ensure date column is datetime
        df[x_col] = pd.to_datetime(df[x_col])
        df['_year'] = df[x_col].dt.year

        # Determine current year
        current_year = self.current_year if self.current_year else df['_year'].max()
        prior_year = current_year - 1

        # Historical years for range calculation (N years before current, excluding current)
        historical_years = list(range(current_year - self.years, current_year))

        # Detect or use specified frequency
        freq = self._normalize_freq(self.freq)
        if freq is None:
            # Try index first if datetime was in index
            if datetime_in_index:
                freq = self._detect_frequency(original_index)
            else:
                freq = self._detect_frequency(df[x_col])

        # Determine if we're using period-based (weekly) or date-based (monthly) alignment
        use_period = self._is_weekly_or_finer(freq)
        x_col_key = '_period' if use_period else '_date'

        # Resample each historical year to mean, then compute min/max/avg across years
        hist_resampled = []
        for year in historical_years:
            year_df = df[df['_year'] == year]
            resampled = self._resample_year(year_df, x_col, y_col, freq, current_year)
            if len(resampled) > 0:
                hist_resampled.append(resampled)

        # For faceted plots, only show legend on first facet
        is_first_facet = (row == 1 and col == 1)
        show_legend_here = self.show_legend and is_first_facet

        if hist_resampled:
            # Combine all historical data (each year's period/monthly means)
            hist_combined = pd.concat(hist_resampled, ignore_index=True)

            # Calculate stats by period/date: min/max/mean of the yearly means
            hist_stats = hist_combined.groupby(x_col_key)['_value'].agg(['min', 'max', 'mean']).reset_index()
            hist_stats.columns = [x_col_key, '_min', '_max', '_avg']
            hist_stats = hist_stats.sort_values(x_col_key)

            # Draw ribbon (min/max range)
            fig.add_trace(
                go.Scatter(
                    x=hist_stats[x_col_key],
                    y=hist_stats['_min'],
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip',
                    legendgroup='range',
                ),
                row=row, col=col
            )
            fig.add_trace(
                go.Scatter(
                    x=hist_stats[x_col_key],
                    y=hist_stats['_max'],
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor=f'rgba(128, 128, 128, {self.ribbon_alpha})',
                    name=f'{self.years}-Year Range',
                    showlegend=show_legend_here,
                    legendgroup='range',
                    hovertemplate='%{x}<br>Min: %{customdata[0]:.2f}<br>Max: %{y:.2f}<extra></extra>',
                    customdata=hist_stats[['_min']].values,
                ),
                row=row, col=col
            )

            # Draw average line
            fig.add_trace(
                go.Scatter(
                    x=hist_stats[x_col_key],
                    y=hist_stats['_avg'],
                    mode='lines',
                    line=dict(color=self.avg_color, dash=self.avg_linetype, width=2),
                    name=f'{self.years}-Year Avg',
                    showlegend=show_legend_here,
                    legendgroup='avg',
                    hovertemplate='%{x}<br>Avg: %{y:.2f}<extra></extra>',
                ),
                row=row, col=col
            )

        # Draw prior year line
        prior_df = df[df['_year'] == prior_year]
        prior_resampled = self._resample_year(prior_df, x_col, y_col, freq, current_year)
        if len(prior_resampled) > 0:
            fig.add_trace(
                go.Scatter(
                    x=prior_resampled[x_col_key],
                    y=prior_resampled['_value'],
                    mode='lines',
                    line=dict(color=self.prior_color, width=2),
                    name=str(prior_year),
                    showlegend=show_legend_here,
                    legendgroup='prior',
                    hovertemplate=f'{prior_year}<br>%{{x}}<br>Value: %{{y:.2f}}<extra></extra>',
                ),
                row=row, col=col
            )

        # Draw current year line
        current_df = df[df['_year'] == current_year]
        current_resampled = self._resample_year(current_df, x_col, y_col, freq, current_year)
        if len(current_resampled) > 0:
            fig.add_trace(
                go.Scatter(
                    x=current_resampled[x_col_key],
                    y=current_resampled['_value'],
                    mode='lines',
                    line=dict(color=self.current_color, width=2.5),
                    name=str(current_year),
                    showlegend=show_legend_here,
                    legendgroup='current',
                    hovertemplate=f'{current_year}<br>%{{x}}<br>Value: %{{y:.2f}}<extra></extra>',
                ),
                row=row, col=col
            )

        # Draw additional specified years
        if self.show_years:
            extra_colors = ['green', 'purple', 'orange', 'brown', 'pink', 'cyan', 'magenta']
            color_idx = 0

            for year in self.show_years:
                if year in [current_year, prior_year]:
                    continue  # Skip if already drawn

                year_df = df[df['_year'] == year]
                year_resampled = self._resample_year(year_df, x_col, y_col, freq, current_year)
                if len(year_resampled) > 0:
                    year_color = extra_colors[color_idx % len(extra_colors)]
                    color_idx += 1

                    fig.add_trace(
                        go.Scatter(
                            x=year_resampled[x_col_key],
                            y=year_resampled['_value'],
                            mode='lines',
                            line=dict(color=year_color, width=2),
                            name=str(year),
                            showlegend=show_legend_here,
                            legendgroup=f'year_{year}',
                            hovertemplate=f'{year}<br>%{{x}}<br>Value: %{{y:.2f}}<extra></extra>',
                        ),
                        row=row, col=col
                    )

        # Update x-axis formatting
        if use_period:
            # For weekly data, x-axis is week number (1-52)
            fig.update_xaxes(
                title_text='Week',
                row=row, col=col
            )
        else:
            # For monthly data, show month names
            fig.update_xaxes(
                tickformat='%b',
                dtick='M1',
                row=row, col=col
            )
