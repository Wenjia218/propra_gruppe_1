#!/usr/bin/python3

import argparse as ap

parser = ap.ArgumentParser()

parser.add_argument('--fasta', type=ap.FileType("rt"), required=True)

args = parser.parse_args()
fasta = args.fasta


def join_string(charlist):
    print_string = "".join(charlist)
    return print_string

print(args.fasta.readline().strip("\n").split(" ")[0])

char_list = []
for line in args.fasta:
    if line[0] == ">":
        print(join_string(char_list).strip().replace("T", "U"))
        print(line.strip("\n").split(" ")[0])
        char_list = []
    else:
        char_list.extend(line.strip())
print(join_string(char_list).strip("\n").replace("T", "U"))
