#!/usr/bin/python3.10

from collections import defaultdict
import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument('--fasta', type=ap.FileType("rt"), required=True)
parser.add_argument('--k', action="extend", nargs="+", type=int, required=True)
parser.add_argument('--start', type=int)
args = parser.parse_args()

start = args.start
fasta = args.fasta
k_list = args.k

# read in fasta data
char_list = []
seq_list = []
genes = []
head = ""
for line in args.fasta:
    if line[0] == ">":
        sequence = "".join(char_list).strip()
        if not sequence == "":
            genes.append(head)
            seq_list.append(sequence)
        head = line.split(" ")[0]
        char_list = []
    else:
        char_list.extend(line.strip())
sequence = "".join(char_list).strip()
if not sequence == "":
    genes.append(head)
    seq_list.append(sequence)

# save all k-substrings
k_dict = {}
for k in k_list:
    k_dict[k] = defaultdict(set)
    for j in range(len(seq_list)):
        if start is not None:
            if len(seq_list[j]) - k + 1 > start:
                k_dict[k][seq_list[j][start:start + k]].add(j)
        else:
            for i in range(len(seq_list[j]) - k + 1):
                k_dict[k][seq_list[j][i:i + k]].add(j)

unique_geneset = {}
for k in k_list:
    unique_geneset[k] = set()
    for val in k_dict[k].values():
        if len(val) == 1:
            unique_geneset[k].add(genes[list(val)[0]])
    print(str(k) + "\t" + str(len(unique_geneset[k])))
