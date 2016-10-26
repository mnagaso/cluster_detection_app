#!/usr/bin/env python

'''

This script converts
test node file to .csv

'''

import sys
import csv

outfile = 'test.csv'

def writeOutCsv(infile):
    f = open(infile)
    all_line = f.readlines()
    f.close()

    fout = open(outfile,'w')
    writer = csv.writer(fout, lineterminator='\n')

    stripped = (l.strip() for l in all_line)
    count = 0
    for line in stripped:
        if count == 0:
            count+=1
            continue
        else:
            newline = line.split()
            #print newline
            writer.writerow(newline)
            count+=1
        #print len(line) 


if __name__ == "__main__":    
    try:
        arg1 = sys.argv[1]
        # get the total number of args
        #total = len(sys.argv)

    except IndexError:
        print "Usage: sample2csv.py <arg1>"
        print "arg1 = input file"
        sys.exit(1)

    writeOutCsv(arg1)
