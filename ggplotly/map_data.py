# map_data.py
"""
Map data functions for ggplotly, similar to ggplot2's map_data().

Since Plotly has built-in geographic support, this module provides
helper functions that return map region identifiers that work with
Plotly's Choropleth and Scattergeo traces.
"""

import pandas as pd


def map_data(map_name='state'):
    """
    Get map region data for use with geom_map.

    Similar to ggplot2's map_data() function, but returns region identifiers
    that work with Plotly's built-in geographic support.

    Parameters:
        map_name (str): The map to retrieve. Options:
            - 'state': US state abbreviations
            - 'usa': Alias for 'state'
            - 'world': ISO-3 country codes
            - 'county': US county FIPS codes (placeholder)

    Returns:
        pandas.DataFrame: A dataframe with region identifiers

    Examples:
        >>> from ggplotly import map_data
        >>> states = map_data('state')
        >>> countries = map_data('world')
    """
    if map_name in ('state', 'usa'):
        return _get_us_states()
    elif map_name == 'world':
        return _get_world_countries()
    else:
        raise ValueError(f"Unknown map: {map_name}. Options: 'state', 'usa', 'world'")


def _get_us_states():
    """Return US state data with abbreviations and names."""
    states = [
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
        ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
        ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
        ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
        ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
        ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
        ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
        ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
        ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
        ('WI', 'Wisconsin'), ('WY', 'Wyoming'), ('DC', 'District of Columbia')
    ]
    return pd.DataFrame(states, columns=['id', 'name'])


def _get_world_countries():
    """Return world country data with ISO-3 codes and names."""
    # Common countries with ISO-3 codes
    countries = [
        ('USA', 'United States'), ('CAN', 'Canada'), ('MEX', 'Mexico'),
        ('BRA', 'Brazil'), ('ARG', 'Argentina'), ('CHL', 'Chile'), ('COL', 'Colombia'),
        ('PER', 'Peru'), ('VEN', 'Venezuela'), ('ECU', 'Ecuador'),
        ('GBR', 'United Kingdom'), ('FRA', 'France'), ('DEU', 'Germany'), ('ITA', 'Italy'),
        ('ESP', 'Spain'), ('PRT', 'Portugal'), ('NLD', 'Netherlands'), ('BEL', 'Belgium'),
        ('CHE', 'Switzerland'), ('AUT', 'Austria'), ('POL', 'Poland'), ('SWE', 'Sweden'),
        ('NOR', 'Norway'), ('DNK', 'Denmark'), ('FIN', 'Finland'), ('IRL', 'Ireland'),
        ('GRC', 'Greece'), ('CZE', 'Czech Republic'), ('HUN', 'Hungary'), ('ROU', 'Romania'),
        ('UKR', 'Ukraine'), ('RUS', 'Russia'), ('TUR', 'Turkey'),
        ('CHN', 'China'), ('JPN', 'Japan'), ('KOR', 'South Korea'), ('PRK', 'North Korea'),
        ('IND', 'India'), ('PAK', 'Pakistan'), ('BGD', 'Bangladesh'), ('IDN', 'Indonesia'),
        ('MYS', 'Malaysia'), ('THA', 'Thailand'), ('VNM', 'Vietnam'), ('PHL', 'Philippines'),
        ('SGP', 'Singapore'), ('TWN', 'Taiwan'), ('HKG', 'Hong Kong'),
        ('AUS', 'Australia'), ('NZL', 'New Zealand'),
        ('ZAF', 'South Africa'), ('EGY', 'Egypt'), ('NGA', 'Nigeria'), ('KEN', 'Kenya'),
        ('ETH', 'Ethiopia'), ('TZA', 'Tanzania'), ('MAR', 'Morocco'), ('DZA', 'Algeria'),
        ('SAU', 'Saudi Arabia'), ('ARE', 'United Arab Emirates'), ('ISR', 'Israel'),
        ('IRN', 'Iran'), ('IRQ', 'Iraq'), ('QAT', 'Qatar'), ('KWT', 'Kuwait'),
    ]
    return pd.DataFrame(countries, columns=['id', 'name'])
