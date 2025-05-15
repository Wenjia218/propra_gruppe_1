#!/usr/bin/python3

import argparse
import collections
import os.path
import pathlib
import sys
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--id', type=str, help='PDB ID', default=sys.stdin)
parser.add_argument('--output', type=pathlib.Path, help='path to output')
parser.add_argument('--fasta', action='store_true', help='add this option to output in fasta format', default=False)
args = parser.parse_args()

aa_dict = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'MET': 'M', 'LEU': 'L', 'LYS': 'K', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}

url = f'https://files.rcsb.org/download/{args.id}.pdb'
with urllib.request.urlopen(url) as response:
    data = response.read()
    data = data.decode('utf-8', 'ignore')

    path_out = os.path.join(args.output, f'{args.id}.pdb')

    if args.fasta:
        path_out = f'{path_out[:-3]}fasta'

        fasta = collections.defaultdict(list)

        # ref https://www.wwpdb.org/documentation/file-format-content/format33/sect3.html#SEQRES
        for line in data.split('\n'):
            if line[:6] == 'SEQRES':
                for aa in line[19:70].split():
                    if aa in aa_dict.keys():
                        fasta[line[11]].append(aa_dict[aa])

        data = []
        for (key, value) in fasta.items():
            data.append(f'>{args.id} {key}')
            data.append(''.join(value))
        data = '\n'.join(data)

    if args.output.name == '-':
        print(data)
    else:
        with open(path_out, 'wt') as file_out:
            for line in data:
                file_out.write(line)
