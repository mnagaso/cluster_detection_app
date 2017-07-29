#!/bin/sh

../benchmark -f flag_n8000.dat
mv network.dat n8000_network.dat
python ./../../sample2csv.py n8000_network.dat new_n8000
cp ./*.csv ./../../../../enot_clustering/data/

