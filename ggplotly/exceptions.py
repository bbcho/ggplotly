"""
Custom exceptions for ggplotly.

This module provides helpful, actionable error messages to guide users
when they make common mistakes with aesthetic mappings, data, or parameters.
"""

from difflib import get_close_matches


class GgplotlyError(Exception):
    """Base exception for all ggplotly errors."""
    pass


class AestheticMappingError(GgplotlyError):
    """Base exception for aesthetic mapping errors."""
    pass


class ColumnNotFoundError(AestheticMappingError):
    """
    Raised when a mapped column doesn't exist in the data.

    Provides suggestions for similar column names to help with typos.
    """

    def __init__(self, column: str, available_columns: list, aesthetic: str = None):
        self.column = column
        self.available_columns = list(available_columns)
        self.aesthetic = aesthetic

        # Find similar column names
        similar = get_close_matches(column, self.available_columns, n=3, cutoff=0.4)

        # Build error message
        msg_parts = [f"Column '{column}' not found in data."]

        if aesthetic:
            msg_parts[0] = f"Column '{column}' for aesthetic '{aesthetic}' not found in data."

        # Show available columns (limit to 10 for readability)
        if len(self.available_columns) <= 10:
            msg_parts.append(f"Available columns: {self.available_columns}")
        else:
            msg_parts.append(f"Available columns: {self.available_columns[:10]}... ({len(self.available_columns)} total)")

        # Suggest similar names
        if similar:
            if len(similar) == 1:
                msg_parts.append(f"Did you mean: '{similar[0]}'?")
            else:
                msg_parts.append(f"Did you mean one of: {similar}?")

        self.message = "\n".join(msg_parts)
        super().__init__(self.message)


class InvalidColorError(AestheticMappingError):
    """
    Raised when a color value is not recognized.

    Provides guidance on valid color formats.
    """

    def __init__(self, color: str):
        self.color = color
        self.message = (
            f"Color '{color}' not recognized.\n"
            f"Valid formats:\n"
            f"  - Hex colors: '#FF0000', '#ff0000'\n"
            f"  - RGB: 'rgb(255, 0, 0)'\n"
            f"  - RGBA: 'rgba(255, 0, 0, 0.5)'\n"
            f"  - Named colors: 'red', 'blue', 'steelblue', 'forestgreen'\n"
            f"  - Plotly colors: Any color from plotly.colors"
        )
        super().__init__(self.message)


class InvalidAestheticError(AestheticMappingError):
    """
    Raised when an aesthetic value is invalid for its type.
    """

    def __init__(self, aesthetic: str, value, expected: str, hint: str = None):
        self.aesthetic = aesthetic
        self.value = value
        self.expected = expected

        msg_parts = [
            f"Invalid value for aesthetic '{aesthetic}': {value!r}",
            f"Expected: {expected}"
        ]

        if hint:
            msg_parts.append(f"Hint: {hint}")

        self.message = "\n".join(msg_parts)
        super().__init__(self.message)


class FacetError(GgplotlyError):
    """Base exception for faceting errors."""
    pass


class FacetColumnNotFoundError(FacetError):
    """
    Raised when a facet variable doesn't exist in the data.
    """

    def __init__(self, column: str, available_columns: list, facet_type: str = "facet"):
        self.column = column
        self.available_columns = list(available_columns)

        similar = get_close_matches(column, self.available_columns, n=3, cutoff=0.4)

        msg_parts = [f"Facet variable '{column}' not found in data."]

        if len(self.available_columns) <= 10:
            msg_parts.append(f"Available columns: {self.available_columns}")
        else:
            msg_parts.append(f"Available columns: {self.available_columns[:10]}...")

        if similar:
            msg_parts.append(f"Did you mean: '{similar[0]}'?")

        self.message = "\n".join(msg_parts)
        super().__init__(self.message)


class TooManyFacetsWarning(UserWarning):
    """
    Warning when a facet variable has many unique values.

    This is a warning rather than an error since it may be intentional.
    """
    pass


class RequiredAestheticError(GgplotlyError):
    """
    Raised when a required aesthetic is missing.
    """

    def __init__(self, geom_name: str, missing_aesthetics: list, example: str = None):
        self.geom_name = geom_name
        self.missing_aesthetics = missing_aesthetics

        msg_parts = [
            f"{geom_name} requires aesthetics: {missing_aesthetics}",
            f"Add them using aes(). Example: aes({', '.join(f'{a}=\"column_name\"' for a in missing_aesthetics)})"
        ]

        if example:
            msg_parts.append(f"Full example: {example}")

        self.message = "\n".join(msg_parts)
        super().__init__(self.message)


class ScaleError(GgplotlyError):
    """Base exception for scale errors."""
    pass


class InvalidScaleParameterError(ScaleError):
    """
    Raised when a scale parameter is invalid.
    """

    def __init__(self, scale_name: str, param_name: str, value, expected: str):
        self.scale_name = scale_name
        self.param_name = param_name
        self.value = value
        self.expected = expected

        self.message = (
            f"Invalid parameter '{param_name}' for {scale_name}: {value!r}\n"
            f"Expected: {expected}"
        )
        super().__init__(self.message)
