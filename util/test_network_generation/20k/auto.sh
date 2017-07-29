#!/bin/sh

../benchmark -f flag_n20k.dat
mv network.dat n20k_network.dat
python ./../../sample2csv.py n20k_network.dat new_n20k
cp ./*.csv ./../../../../enot_clustering/data/

