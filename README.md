[PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT)
=============
Date Created: 3/7/2013<br>
Authors: Michael Musslewhite, Larry Lindsey<br>

# Overview
[PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT) provides easy access to data in XML files associated with the program [RECONSTRUCT](http://synapses.clm.utexas.edu/tools/reconstruct/reconstruct.stm).
This package also contains several tools for managing this data:
* mergeTool - merge series together with built-in conflict resolution
* excelTool - output data into excel workbooks (.xlsx)
* calibrationTool - rescale contours representing images in a section
* curationTool - check for various properties of objects in a series

The functions/tools already in place can be used to develop solutions to a wide range of problems associated with RECONSTRUCT data.

# Install Instructions
*The build found on GitHub is the development build and may be unstable.*<br>
*The stable version can be found here: [PyPI](https://pypi.python.org/pypi/PyRECONSTRUCT) (Python Package Index)*

### Linux
* Install the following dependencies:
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
* Install [PySide](http://qt-project.org/wiki/PySide) *(This can be quite tricky, but there are many tutorials online)*
* Install [PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT) by running `python setup.py install` from the parent folder

### Windows *(discouraged)*
PyRECONSTRUCT for Windows has only been tested using the following method:
* Download and install [Python2.7](http://www.python.org/download/releases/2.7.5/)
* Download and install [python-setuptools](http://python-distribute.org/distribute_setup.py)
* Download [PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT)
* Run `python setup.py install` from parent folder
    * Dependencies will likely be missing, but the errors will tell you what you need
* Download and install [lxml](https://pypi.python.org/packages/2.7/l/lxml/lxml-3.2.3.win-amd64-py2.7.exe#md5=3720e7d124275b728f553eb93831869c)
* Download and install [Cython](http://www.lfd.uci.edu/~gohlke/pythonlibs/#cython)
* Download and install [Scipy-stack](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy-stack)
* Download and install [scikit-image](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scikit-image)
* Download and install [scipy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy)
    * fixes missing scipy.special package
* ...Should work now?
	*email me if there are problems (address located in setup.py)!*


