#!/bin/sh

../benchmark -f flag_n2000.dat
mv network.dat n2000_network.dat
python ./../../sample2csv.py n2000_network.dat new_n2000
cp ./*.csv ./../../../../enot_clustering/data/

