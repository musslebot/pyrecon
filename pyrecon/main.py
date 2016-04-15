"""Main, overarching functions that are used in multiple modules."""
try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    print("Problem importing PySide. You will not be able to use GUI functions.")


def openSeries(path):
    """Returns a Series object with associated Sections from the same directory."""
    import os
    import re
    from pyrecon.classes import Series
    from pyrecon.tools.reconstruct_reader import process_series_file

    if ".ser" in path:
        path = os.path.dirname(path)

    # Gather Series from provided path
    series_files = []
    for filename in os.listdir(path):
        if ".ser" in filename:
            series_files.append(filename)
    assert len(series_files) == 1, "There is more than one Series file in the provided directory"
    series_file = series_files[0]
    series_path = os.path.join(path, series_file)

    series = Series()
    series.name = series_file.replace(".ser", "")
    for k, v in process_series_file(series_path).iteritems():
        if hasattr(series, k):
            setattr(series, k, v)
        else:
            print("Series has no attribute: {}. Skipping.".format(k))

    # Gather Sections from provided path
    section_regex = re.compile(r"{}.[0-9]+$".format(series.name))
    sections = []
    for filename in os.listdir(path):
        if re.match(section_regex, filename):
            section = process(os.path.join(path, filename))
            sections.append(section)
    series.sections = sorted(sections, key=lambda Section: Section.index)

    return series


def start():
    """Begin GUI application (pyrecon.gui.main)"""
    app = QApplication.instance()
    if app is None:  # Create QApplication if doesn"t exist
        app = QApplication([])
    from pyrecon.gui.main import PyreconMainWindow
    gui = PyreconMainWindow()
    app.exec_()  # Start event-loop


if __name__ == "__main__":
    try:
        start()
    except:
        print "Error running start() from main.py -- Did PySide import correctly?"
