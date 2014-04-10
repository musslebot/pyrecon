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
* Download and install [Python2.7](http://www.python.org/download/releases/2.7.6/)
* Download and install [python-setuptools](http://python-distribute.org/distribute_setup.py)
* Download and install the following:
    * [lxml](http://www.lfd.uci.edu/~gohlke/pythonlibs/#lxml)
    * [Cython](http://www.lfd.uci.edu/~gohlke/pythonlibs/#cython)
    * [Scipy-stack](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy-stack)
    * [scikit-image](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scikit-image)
    * [scipy](http://www.lfd.uci.edu/~gohlke/pythonlibs/#scipy)
    * [shapely](http://www.lfd.uci.edu/~gohlke/pythonlibs/#shapely)
* Install PyRECONSTRUCT:
    * **Method 1:** 
        * Download [PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT)
        * Run `python setup.py install` from parent folder
    * **Method 2:**
        * Install [PIP](http://www.pip-installer.org/en/latest/installing.html)
            * you may also need to add `C:\Python27\Scripts;` to your Windows user environment variable: Path
        * Run `pip install PyRECONSTRUCT` in windows command line (cmd.exe)

### PyRECONSTRUCT + Git Installation
* 1) Add the following lines to your Series' repository's `.git/config` file, replacing PATH_TO_gitmerge.py appropriately:
<pre>
[merge "pymerge"]
        name = pyrecon mergetool driver
        driver = PATH_TO_gitmerge.py %A %B
</pre>

* 2) Add the following line to your Series' repository's `.git/info/attributes` file:
<pre>
`* merge=pymerge`


