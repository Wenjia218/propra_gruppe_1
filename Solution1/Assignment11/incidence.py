#!/usr/bin/python3.10

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--sequence', action='extend', nargs='+', type=str, help='sequences to look for')
parser.add_argument('--genome', type=argparse.FileType('rt'), help='genome to look sequences up in')
args = parser.parse_args()

sequences = args.sequence
genome = ''

with open(args.genome.name) as genome_file:
    for line in genome_file:
        if not line.startswith('>'):
            genome += line.strip()
genome = genome.upper()

for s in sequences:
    s = s.upper()
    count = 0
    for i in range(len(genome) - len(s)):
        if genome[i:i+len(s)] == s:
            count += 1
    print('%s: %i' % (s, count))
