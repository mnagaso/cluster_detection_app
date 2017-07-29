#!/bin/sh

../benchmark -f flag_n80000.dat
mv network.dat 80k_network.dat
python ./../../sample2csv.py 80k_network.dat 80k
cp ./*.csv ./../../../../enot_clustering/data/

