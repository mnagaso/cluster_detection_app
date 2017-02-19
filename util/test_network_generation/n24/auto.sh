#!/bin/sh

../benchmark -f flag_new_n24.dat
mv network.dat new_n24_network.dat
python ./../../../Py_template/enot/util/sample2csv.py new_n24_network.dat new_n24
cp ./*.csv ./../../../Py_template/enot/data/

