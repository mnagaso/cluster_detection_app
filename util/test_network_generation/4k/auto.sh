#!/bin/sh

../benchmark -f flag_n4000.dat
mv network.dat n4000_network.dat
python ./../../sample2csv.py n4000_network.dat new_n4000
cp ./*.csv ./../../../../enot_clustering/data/

