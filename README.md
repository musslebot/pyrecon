[PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT)
=============
Authors: Michael Musslewhite, Larry Lindsey<br>
Date Created: 3/7/2013<br>


# Overview
[PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT) provides easy access to data in XML files associated with the program [RECONSTRUCT](http://synapses.clm.utexas.edu/tools/reconstruct/reconstruct.stm).
This package also contains several tools for managing this data:
* mergeTool - merge series together with built-in conflict resolution (graphical or non-graphical)
* excelTool - output data into excel workbooks (.xlsx)
* calibrationTool - rescale contours representing images in a section
* curationTool - check for various properties of objects in a series

The functions/tools already in place can be used to develop solutions to a wide range of problems associated with RECONSTRUCT data.

To start graphical tool loader, use commands in python shell:
* `import pyrecon`
* `pyrecon.start()`

# Install Instructions
*The most stable version can also be found here: [PyPI](https://pypi.python.org/pypi/PyRECONSTRUCT) (Python Package Index)*

### Linux
* Install the following dependencies (through `apt-get` or other package manager):
    * `python-dev`
    * `python-setuptools`
    * `libgeos-dev`
    * `libblas-dev`
    * `liblapack-dev`
    * `libfreetype6-dev`
    * `libpng-dev`
    * `gfortran`
    * `libxml2-dev`
    * `libxslt-dev`
    * `cmake`
    * `libshiboken-dev`
* Install [PySide](http://qt-project.org/wiki/PySide)
* Install [PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT) by running `python setup.py install` from its parent folder

### Windows
* COMING SOON
* Download this repository
* Run 'PyRECONSTRUCT Installer.exe'
* No other files/folders in the repository are necessary... feel free to remove them 

### PyRECONSTRUCT + Git
* IN DEVELOPMENT...


