#!/bin/sh

./pyx2py.sh
rm *.so
rm ./lib/*.c
rm -rf ./build
