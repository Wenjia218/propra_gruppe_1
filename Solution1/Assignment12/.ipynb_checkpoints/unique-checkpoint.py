#!/usr/bin/python3.10

from collections import defaultdict
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument('--fasta', type=ap.FileType("rt"))
parser.add_argument('--k', action="extend", nargs="+", type=int)
args = parser.parse_args()

fasta = args.fasta
k_list = args.k

# read in fasta data
char_list = []
seq_list = []
genes = []
for line in args.fasta:
    if line[0] == ">":
        genes.append(args.fasta.readline().strip("> \n\t"))
        seq_list.append("".join(char_list).strip())
        char_list = []
    else:
        char_list.extend(line.strip())
seq_list.append("".join(char_list).strip())
seq_list.pop(0)

# save all k-substrings
k_dict = {}
for k in k_list:
    k_dict[k] = defaultdict(set)
    for j in range(len(seq_list)):
        for i in range(len(seq_list[j]) - k + 1):
            k_dict[k][seq_list[j][i:i + k]].add(j)

unique_geneset = {}
for k in k_list:
    unique_geneset[k] = set()
    for val in k_dict[k].values():
        if len(val) == 1:
            unique_geneset[k].add(genes[list(val)[0]])
    print(str(k) + "\t" + str(len(unique_geneset[k])))

