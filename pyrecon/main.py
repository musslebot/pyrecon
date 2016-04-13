"""Main, overarching functions that are used in multiple modules."""
try:
    from PySide.QtCore import *
    from PySide.QtGui import *
except:
    print("Problem importing PySide. You will not be able to use GUI functions.")


def openSeries(path):
    """Returns a Series object with associated Sections from the same directory."""
    from pyrecon.classes import Series
    import os
    # Process <path> and create Series object
    if ".ser" in path: # Search path for .ser
        pathToSeries = path
    else: # or .ser in directory path?
        if path[-1] != "/":
            path += "/"
        pathToSeries = path+str([f for f in os.listdir(path) if ".ser" in f].pop())
    series = Series(pathToSeries)
    series.update(sections=True) # find sections in directory
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
