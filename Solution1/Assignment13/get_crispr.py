#!/usr/bin/python3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--fasta')
args = parser.parse_args()
fasta = args.fasta


# read fasta and save the sequence in sequences{}
def read_fasta(f):
    sequences = {}
    active_sequence_name = ""
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            active_sequence_name = line[1:]
            if active_sequence_name not in sequences:
                sequences[active_sequence_name] = ""
            continue
        sequence = line
        sequences[active_sequence_name] = sequences[active_sequence_name] + sequence
    return sequences

with open(fasta, "r") as f:
    sequences = read_fasta(f)

record_name = ""
start_position = 0
seq = ""

for key in sequences:
    record_name = key
    value = sequences[key]

    for i in range (21, len(value)-1):
        if (value[i] == 'G') and (value[i + 1] == 'G'):
            seq = value[i - 21 : i + 2]
            start_position = i - 20
            print(">" + record_name + '\t' + str(start_position) + '\n' + seq )



