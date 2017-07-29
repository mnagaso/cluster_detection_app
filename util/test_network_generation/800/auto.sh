#!/bin/sh

../benchmark -f flag_new_n800.dat
mv network.dat new_n800_network.dat
python ./../../sample2csv.py new_n800_network.dat new_n800
cp ./*.csv ./../../../../enot_clustering/data/

