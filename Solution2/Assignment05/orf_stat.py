#!/usr/bin/python3

import argparse as ap
import sys
import matplotlib.pyplot as plt

parser = ap.ArgumentParser()
parser.add_argument('--fasta', type=ap.FileType("rt"), required=False, default=sys.stdin)
parser.add_argument('--histogram', type=str, required=False)
parser.add_argument('--lower', type=int, required=True)
parser.add_argument('--upper', type=int, required=True)
parser.add_argument('--bins', type=int, required=True)

args = parser.parse_args()

# read in fasta data
char_list = []
seq_list = []
orfs = []
head = ""
for line in args.fasta:
    if line[0] == ">":
        sequence = "".join(char_list).strip()
        if not sequence == "":
            orfs.append(head.strip())
            seq_list.append(sequence)
        head = line.split(" ")[0]
        char_list = []
    else:
        char_list.extend(line.strip())
sequence = "".join(char_list).strip()
if not sequence == "":
    orfs.append(head.strip())
    seq_list.append(sequence)

coding_orf_counter = 0
coding_orfs = []
for orf_seq in seq_list:
    if (len(orf_seq) // 3 - 2 <= args.upper) and (len(orf_seq) // 3 - 2 >= args.lower):
        coding_orf_counter += 1
        coding_orfs.append(len(orf_seq) // 3 - 2)
print(coding_orf_counter)

if args.histogram is not None:
    bins = round((args.upper - args.lower) / args.bins)
    plt.hist(coding_orfs, bins=bins)
    # plt.xlim(args.lower)
    plt.savefig(args.histogram)

