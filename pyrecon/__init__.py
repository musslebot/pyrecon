"""Main, overarching functions that are used in multiple modules."""


def openSeries(path):
    """Returns a Series object with associated Sections from the same directory."""
    import os
    from pyrecon.tools.reconstruct_reader import process_series_directory

    if ".ser" in path:
        path = os.path.dirname(path)

    series = process_series_directory(path)

    return series

