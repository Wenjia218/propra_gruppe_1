#!/usr/bin/python3

import argparse as ap
import sys
import pymysql

parser = ap.ArgumentParser()
parser.add_argument('--fasta', type=ap.FileType("rt"), required=False, default=sys.stdin)
parser.add_argument('--db', action='store_true', default=False, required=False)
parser.add_argument('--output', type=ap.FileType("w"), required=False, default=sys.stdout)

args = parser.parse_args()

# read in fasta data
char_list = []
seq_list = []
genes = []
head = ""
for line in args.fasta:
    if line[0] == ">":
        sequence = "".join(char_list).strip()
        if not sequence == "":
            genes.append(head.strip())
            seq_list.append(sequence)
        head = line.split(" ")[0]
        char_list = []
    else:
        char_list.extend(line.strip())
sequence = "".join(char_list).strip()
if not sequence == "":
    genes.append(head.strip())
    seq_list.append(sequence)

# tuples (start_index, end_index)
global orf_locations
orf_locations = []


def find_codons(sequence_dna, frameshift=0, head_index=0, is_reversed=False):
    base_index = frameshift
    start = 0
    end = 0
    # w für "write"
    w = False
    while base_index < len(sequence_dna) - 2:
        codon = "".join(sequence_dna[base_index:base_index + 3])
        if (not w) and (codon == "ATG"):
            print(genes[0] + "_" + str(head_index), file=args.output)
            head_index += 1
            w = True
            start = base_index
        elif codon in {"TAA", "TGA", "TAG"} and w:
            print(codon, file=args.output)
            w = False
            end = base_index + 2
            if not is_reversed:
                orf_locations.append((start, end))
            else:
                orf_locations.append((len(sequence_dna) - 1 - start, len(sequence_dna) - 1 - end))

        if w:
            args.output.write(codon)
        base_index += 3
    return head_index


# reverse complement of dna sequence
sequence_dna_r = []
for char in list(seq_list[0][::-1]):
    if char == 'A':
        sequence_dna_r.append('T')

    elif char == 'T':
        sequence_dna_r.append('A')

    elif char == 'G':
        sequence_dna_r.append('C')

    elif char == 'C':
        sequence_dna_r.append('G')
sequence_dna_r = "".join(sequence_dna_r)

# index for ORF naming
orf_name = 0

for i in range(3):
    orf_name = find_codons(seq_list[0], i, orf_name)
    orf_name = find_codons(sequence_dna_r, i, orf_name, True)

if args.db:
    db = pymysql.connect(host="127.0.0.1", user="bioprakt01",
                         passwd="$1$io6mhFO5$MqQTA.eOzVMh2hDdllQij/", database="bioprakt01", port=3307)
    cursor = db.cursor()
    cursor.execute("INSERT INTO Sequences VALUES (bioclient1, " + genes[0] + ", " + seq_list[0] + ", " + "Yeast" + ");")
    for start, end in orf_locations:
        cursor.execute("INSERT INTO ORFs VALUES (bioclient1, " + genes[0] + ", " + str(start) + ", " + str(end) + ");")
    db.close()
