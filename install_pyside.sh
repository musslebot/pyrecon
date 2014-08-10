#!/bin/bash
sudo apt-get install build-essential git libqt4-dev libphonon-dev libxslt1-dev qtmobility-dev &&
wget https://pypi.python.org/packages/source/P/PySide/PySide-1.2.2.tar.gz &&
tar -xvzf PySide-1.2.2.tar.gz &&
cd PySide-1.2.2 &&
python setup.py install
cd ..

