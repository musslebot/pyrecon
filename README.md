![alt text](https://github.com/musslebot/pyrecon/raw/master/icon.ico "PyRECONSTRUCT Icon")[PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT)
=============
Authors: Michael Musslewhite, Larry Lindsey<br>
Date Created: 3/7/2013<br>

# Overview
[PyRECONSTRUCT](https://pypi.python.org/pypi/PyRECONSTRUCT) provides easy access to data in XML files associated with the program [RECONSTRUCT](http://synapses.clm.utexas.edu/tools/reconstruct/reconstruct.stm).
* [mergeTool](https://github.com/musslebot/pyrecon/blob/master/pyrecon/tools/mergeTool/mergeTool.md) - merge series together with built-in conflict resolution (graphical or non-graphical)

The functions/tools already in place can be used to develop solutions to a wide range of problems associated with RECONSTRUCT data.

To start the mergetool, use commands in a terminal:
python start.py

# Install Instructions

### Windows
Windows Executable

To install PyRECONSTRUCT on Windows, you must first download [Python 3.6](https://www.python.org/downloads/)

Next, use the [PyRECONSTRUCT.exe](https://drive.google.com/file/d/0B5WELYTJ58RMdVloay1DQm1zUlU/view?usp=sharing)

That's all!

### Linux
linux dependencies:
<code>
python-dev python2.7-dev python-setuptools build-essential libgeos-dev
libblas-dev liblapack-dev libfreetype6-dev libpng-dev gfortran libxml2-dev
libxslt1-dev cmake libshiboken-dev libphonon-dev libqt4-dev qtmobility-dev
</code>

* From the <b>top-level</b> pyrecon directory, run the following commands in a terminal:
<pre>
# After installing dependencies listed above
pip install -r requirements.txt
</pre>
