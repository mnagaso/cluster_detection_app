#!/usr/bin/env python

'''

This script converts
test node file to .csv

'''

import sys
import csv

#outfile = 'test.csv'

def writeOutCsv_edges(infile,outheader):
    f = open(infile)
    all_line = f.readlines()
    f.close()
    
    outfile = outheader + ".csv"

    fout = open(outfile,'w')
    writer = csv.writer(fout, lineterminator='\n')

    stripped = (l.strip() for l in all_line)
    count = 0
    max_id = 0
    for line in stripped:
        if line[0].isdigit() != True: # skip a line with strings
            count+=1
            continue
        else:
            newline = line.split()
            #print (newline)
            id_to = int(newline[0])
            id_from = int(newline[1])
            if id_to > max_id:
                max_id = id_to
            elif id_from > max_id:
                max_id = id_from


            writer.writerow(newline)
            count+=1
        #print len(line) 
    return max_id

def convertOutCsv_vertices(outheader, name_file):
    outfile = outheader + "_vertices.csv"
    fout = open(outfile, 'w')
    writer = csv.writer(fout, lineterminator='\n')

    pass # implement later

def createOutCsv_vertices(outheader, num_node):
    outfile = outheader + "_vertices.csv"
    fout = open(outfile, 'w')
    writer = csv.writer(fout, lineterminator='\n')

    for line in range(num_node):
        row_to_write = [line+1,"id_"+str(line+1)]
        writer.writerow(row_to_write)
    
    fout.close()

if __name__ == "__main__":    
    generate_namelist = False
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        # get the total number of args
        total = len(sys.argv)
        print(total)
        if total == 4:
            arg3 = sys.argv[3]
            
        else:
            generate_namelist = True

    except IndexError:
        print ("Usage: sample2csv.py <arg1> <arg2> <arg3:optional>")
        print ("arg1 = input file, arg2 = output name (#fileheader only, exclude extention ie .csv)")
        print ("optional: arg3 = nodes' name list file with the format:")
        print ("1, name1")
        print ("2, name2")
        print ("...")
        print ("id, name_id")
        print ("name list will be generated automatically if it was not specified.")
        sys.exit(1)

    num_node =  writeOutCsv_edges(arg1, arg2)
    if generate_namelist == True: # create a node id-name list from arg1
        createOutCsv_vertices(arg2, num_node)
    else: # use a pre-existing id-name file
        convertOutCsv_vertices(arg2, arg3)
