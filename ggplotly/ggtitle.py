# ggtitle.py

from .guides import Labs


def ggtitle(title, subtitle=None):
    """
    Function to create a Labs object with a title (and optional subtitle).

    Parameters:
        title (str): The main title of the plot.
        subtitle (str): Optional subtitle to add below the main title.

    Returns:
        Labs: A Labs object with the title and optional subtitle set.
    """
    return Labs(title=title, subtitle=subtitle)
