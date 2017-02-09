#!/bin/sh
./py2pyx.sh
python setup.py build_ext --inplace
