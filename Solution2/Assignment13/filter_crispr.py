#!/usr/bin/env python3

import argparse as ap
import sys
from contextlib import redirect_stdout

def filter_alignments():

    parser = ap.ArgumentParser()
    parser.add_argument('--sam', type=ap.FileType("r"), default=sys.stdin)  # nargs for allowing multiple keywords
    parser.add_argument('--no-off-targets',dest="a", type=ap.FileType("w"), default=sys.stdout)
    parser.add_argument('--with-mismatch', type=ap.FileType("w"), default=sys.stdout)

    args = parser.parse_args()
    
    no_off_targets_seq = {}           # list for recognized sequences (Erkennungssequenzen) that have more than 3 mismatches
    with_missmatch = {}        # list for recognized sequences with smaller than 3 mismatches and gg suffix error

    for line in args.sam:
        line.split("\t")        #every column is divided by tab 
        
        id = ">" + str(line[0])                # save id for fasta format
        missmatch_read = line[13]       #shows how many mismatches are found 
        recognized_seq_read = line[9]    # saves the recognized sequence 
        
        missmatch_val = missmatch_read[5:]      #remove the unnecessary characters
        
        if not (missmatch_val < 4 and recognized_seq_read[-2] != "GG"):   # when is off_target
            no_off_targets_seq[id]= recognized_seq_read
        
        else: 
            with_missmatch[id] = recognized_seq_read


        for key,value in no_off_targets_seq:

            with open(args.a.name,"w") as f:
                with redirect_stdout(f):
                    print(key + "\n" + value)

        for key,value in with_missmatch:

            with open(args.b.name,"w") as f:
                with redirect_stdout(f):
                    print(key + "\n" + value)




        
        
        