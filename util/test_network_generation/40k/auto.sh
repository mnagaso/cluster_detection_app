#!/bin/sh

../benchmark -f flag_n40k.dat
mv network.dat n40k_network.dat
python ./../../sample2csv.py n40k_network.dat new_n40k
cp ./*.csv ./../../../../enot_clustering/data/

