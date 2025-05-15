#!/usr/bin/python3

import argparse
import math
import pathlib
import urllib.request
import sys
from collections import defaultdict
import matplotlib.pyplot as plt

# pdb ref https://www.wwpdb.org/documentation/file-format-content/format23/sect5.html
# to SST classification https://en.wikipedia.org/wiki/Protein_secondary_structure#SST[13]_classification
ss_dict = {
    'HELIX': {
        '1': 'H',  # right-handed alpha
        '2': '?',  # right-handed omega
        '3': 'I',  # right-handed pi
        '4': '?',  # right-handed gamma
        '5': 'G',  # right-handed 310
        '6': 'h',  # left-handed alpha
        '7': '?',  # left-handed omega
        '8': '?',  # left-handed gamma
        '9': '?',  # 27 ribbon/helix
        '10': '?'  # polyproline
    },
    'SHEET': 'E',
    'TURN': 'T'
}

aa_dict = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'MET': 'M', 'LEU': 'L', 'LYS': 'K', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}


def calc_dist(x1, x2, y1, y2, z1, z2):
    dx = x2 - x1
    dy = y2 - y1
    dz = z2 - z1
    return math.sqrt(dx * dx + dy * dy + dz * dz)


parser = argparse.ArgumentParser()
parser.add_argument('--id', type=str, help='PDB-ID', required=True)
parser.add_argument('--distance', type=int, help='max distance', required=True)
parser.add_argument('--type', type=str, help='atom type', required=True)
parser.add_argument('--length', type=int, help='max diff in sequence for local contact', required=True)
parser.add_argument('--output', type=pathlib.Path, help='output directory', default=sys.stdout)
args = parser.parse_args()

sscc_data = []
sscc_keys = ['chain', 'pos', 'serial', 'aa', 'ss', 'global', 'local']

chains = dict()

# name explains itself :)
contact_matrix = defaultdict(dict)

url = f'https://files.rcsb.org/download/{args.id}.pdb'
with urllib.request.urlopen(url) as response:
    data = response.read().decode('utf-8', 'ignore')

    for line in data.split('\n'):
        if len(line):
            record = line[0:6].strip()

            # start list for each chain to collect secondary structure data later
            # ref https://www.wwpdb.org/documentation/file-format-content/format33/sect3.html
            if record == 'SEQRES':
                chain_id = line[11]
                if chain_id not in chains.keys():
                    chain_len = int(line[13:17].strip())
                    chains[chain_id] = ['C' for _ in range(chain_len)]  # set Coil as default secondary structure

            # map different secondary structure elements back to chain and position
            # ref https://www.wwpdb.org/documentation/file-format-content/format23/sect5.html
            elif record == 'HELIX':
                chain_id = line[19]  # assumes that start and end are on the same chain...
                helix_start = int(line[21:25].strip())
                helix_end = int(line[33:37].strip())
                helix_class = line[38:40].strip()
                for i in range(helix_start - 1, helix_end):
                    chains[chain_id][i] = ss_dict[record][helix_class]
            elif record == 'SHEET':
                chain_id = line[21]
                sheet_start = int(line[22:26].strip())
                sheet_end = int(line[33:37].strip())
                for i in range(sheet_start - 1, sheet_end):
                    chains[chain_id][i] = ss_dict[record]
            elif record == 'TURN':
                chain_id = line[19]
                turn_start = int(line[20:24].strip())
                turn_end = int(line[31:35].strip())
                for i in range(turn_start - 1, turn_end):
                    chains[chain_id][i] = ss_dict[record]

            # retrieve atom data
            # ref https://pdb101.rcsb.org/learn/guide-to-understanding-pdb-data/dealing-with-coordinates
            # ref https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html
            elif record == 'ATOM':
                atom_type = line[12:16].strip()
                if atom_type == args.type and (line[16] == 'A' or not len(line[16].strip())):  # only first conformation
                    atom_id = line[6:11].strip()
                    amino_acid = aa_dict[line[17:20]]
                    chain_id = line[21]
                    position = int(line[22:26].strip())
                    secondary_structure = chains[chain_id][position - 1]

                    global_contacts = 0
                    local_contacts = 0
                    x = float(line[30:38].strip())
                    y = float(line[38:46].strip())
                    z = float(line[46:54].strip())

                    # for contact_matrix j, does not change during process
                    j = str(chain_id) + str(position)
                    contact_matrix[j][j] = -1

                    # check for possible contact partners in recorded atoms
                    for atom in sscc_data:
                        # for contact matrix c(i, j)
                        i = str(atom['chain']) + str(atom['pos'])

                        dist = calc_dist(atom['x'], x, atom['y'], y, atom['z'], z)
                        contact_matrix[i][j] = dist
                        contact_matrix[j][i] = dist
                        if dist < args.distance:
                            pos_diff = abs(atom['pos'] - position)

                            if pos_diff < args.length:
                                atom['local'] += 1
                                local_contacts += 1
                            else:
                                atom['global'] += 1
                                global_contacts += 1

                    # add atom data
                    sscc_data.append({
                        'chain': chain_id,
                        'pos': position,
                        'serial': atom_id,
                        'aa': amino_acid,
                        'ss': secondary_structure,
                        'global': global_contacts,
                        'local': local_contacts,
                        'x': x,
                        'y': y,
                        'z': z
                    })

            elif record == 'ENDMDL':
                break


with open("contact_matrix_" + args.id + ".tsv", "w") as cm:
    cm.write("#")
    for key in contact_matrix.keys():
        a_key = key
        cm.write("\t" + key)
    cm.write("\n")
    for j in contact_matrix[a_key].keys():
        cm.write(j)
        for i in contact_matrix.keys():
            if contact_matrix[i][j] < args.distance:
                value = "1"
            else:
                value = "0"
            cm.write("\t" + value)
        cm.write("\n")


plot_matrix = []
for key_i in contact_matrix.keys():
    plot_matrix.append(list(contact_matrix[key_i].values()))

plt.imshow(plot_matrix, cmap='Blues_r', interpolation='nearest')
plt.savefig(args.id + "_plot.png")

# print to console
print('\t'.join(sscc_keys), file=args.output)
for atom in sscc_data:
    text_out = []
    for key in sscc_keys:
        text_out.append(str(atom[key]))
    print('\t'.join(text_out), file=args.output)
