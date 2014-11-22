#!/bin/bash
# This file exists to reduce the PySide installation process into one command
# The downside is that it will occasionally need to be maintained in order to
# account for changes to versions and/or paths
# The current instructions are from this site:
# http://pyside.readthedocs.org/en/latest/building/linux.html
echo '>>> DOWNLOADING PYSIDE PREREQUISITES <<<' &&
sudo apt-get install build-essential git cmake libqt4-dev libphonon-dev python2.7-dev libxml2-dev libxslt1-dev qtmobility-dev
wget https://bootstrap.pypa.io/get-pip.py &&
sudo python2.7 get-pip.py &&
echo '>>> DOWNLOADING PYSIDE <<<' &&
sudo pip2.7 install wheel &&
wget https://pypi.python.org/packages/source/P/PySide/PySide-1.2.2.tar.gz &&
tar -xvzf PySide-1.2.2.tar.gz &&
cd PySide-1.2.2/ &&
echo '>>> BUILDING PYSIDE <<<' &&
sudo python2.7 setup.py bdist_wheel --qmake=/usr/bin/qmake-qt4 &&
cd .. &&
echo '>>> INSTALLING PYSIDE <<<' &&
sudo pip2.7 install PySide-1.2.2/dist/PySide-1.2.2-cp27-none-linux_x86_64.whl &&
sudo python2.7 PySide-1.2.2/pyside_postinstall.py -install &&
echo '>>> CLEANING UP <<<' &&
sudo rm -rf PySide-1.2.2/ &&
sudo rm PySide-1.2.2.tar.gz* &&
sudo rm get-pip.py*
