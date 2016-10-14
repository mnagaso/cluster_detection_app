#!/bin/sh

export AUTOMAKE="automake --foreign -a"
autoreconf -f -i -v

mkdir build
cd build
../configure
make
