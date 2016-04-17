"""Main, overarching functions that are used in multiple modules."""
try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    print("Problem importing PySide. You will not be able to use GUI functions.")


def openSeries(path):
    """Returns a Series object with associated Sections from the same directory."""
    import os
    from pyrecon.tools.reconstruct_reader import process_series_directory

    if ".ser" in path:
        path = os.path.dirname(path)

    series = process_series_directory(path)

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
