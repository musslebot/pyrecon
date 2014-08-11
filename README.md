![alt text](https://github.com/wtrdrnkr/pyrecon/raw/master/icon.ico "PyRECONSTRUCT Icon")[PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT)
=============
Authors: Michael Musslewhite, Larry Lindsey<br>
Date Created: 3/7/2013<br>

# Overview
[PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT) provides easy access to data in XML files associated with the program [RECONSTRUCT](http://synapses.clm.utexas.edu/tools/reconstruct/reconstruct.stm).
This package also contains several tools for managing this data:
* [gitTool](https://github.com/wtrdrnkr/pyrecon/blob/docs/pyrecon/tools/gitTool/gitTool.md) - Reduced functionality UI for interacting with a git repository containing a Series
* [mergeTool](https://github.com/wtrdrnkr/pyrecon/blob/docs/pyrecon/tools/mergeTool/mergeTool.md) - merge series together with built-in conflict resolution (graphical or non-graphical)
* [excelTool](https://github.com/wtrdrnkr/pyrecon/blob/docs/pyrecon/tools/excelTool/excelTool.md) - output data into excel workbooks (.xlsx)
* [calibrationTool](https://github.com/wtrdrnkr/pyrecon/blob/docs/pyrecon/tools/calibrationTool/calibrationTool.md) - rescale contours representing images in a section
* [curationTool](https://github.com/wtrdrnkr/pyrecon/blob/docs/pyrecon/tools/curationTool/curationTool.md) - check for various properties of objects in a series

The functions/tools already in place can be used to develop solutions to a wide range of problems associated with RECONSTRUCT data.

To start graphical tool loader, use commands in python shell:
* `import pyrecon`
* `pyrecon.start()`

# Install Instructions
*The most stable version can also be found here: [PyPI](https://pypi.python.org/pypi/PyRECONSTRUCT) (Python Package Index)*

### Linux
* From the <b>top-level</b> pyrecon directory, run the following commands in a terminal:
<pre>
sudo ./install_depends.sh  # Installs linux package dependencies
./install_prereqs.sh  # Installs python packages
sudo ./install_pyside.sh  # Install PySide
python setup.py install
</pre>

### Windows
* Send me a message for the PyRECONSTRUCT Windows Installer.exe -- filesize is too large to keep in GitHub
