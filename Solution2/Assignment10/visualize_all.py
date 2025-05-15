#!/usr/bin/python3.10

import argparse
import math
import os.path
import pathlib
import subprocess
import urllib.request


def calc_dist(d_x, d_y, d_z):
    return math.sqrt(d_x ** 2 + d_y ** 2 + d_z ** 2)


parser = argparse.ArgumentParser()
parser.add_argument('--id', action='extend', nargs='+', type=str, help='PDB-IDs to retrieve', required=True)
parser.add_argument('--output', type=pathlib.Path, help='optional directory to save all pictures in')
args = parser.parse_args()

pdb_ids = args.id
for pdb_id in pdb_ids:
    url = f'https://files.rcsb.org/download/{pdb_id}.pdb'
    with urllib.request.urlopen(url) as response:
        pdb_data = response.read().decode('utf-8', 'ignore')
        pdb_filepath = f'{pdb_id}.pdb'  # os.path.join('tmp', f'{pdb_id}.pdb')
        protein = dict()
        with open(pdb_filepath, 'wt') as pdb_file:
            chain_id = None
            protein['sec_str'] = 0
            protein['known_coord'] = set()
            first_CA = True
            first_CB = True
            for line in pdb_data.split('\n'):
                pdb_file.write(f'{line}\n')

                if len(line.strip()):
                    line = line.strip().split()

                    # sequence/chain attributes
                    if line[0] == 'DBREF' and chain_id is None:
                        chain_id = line[2]
                        protein['len'] = int(line.pop())

                    # secondary structure elements
                    # ref https://www.wwpdb.org/documentation/file-format-content/format23/sect5.html
                    elif line[0] == 'HELIX':
                        protein['sec_str'] += int(line.pop())
                    elif line[0] == 'SHEET':
                        protein['sec_str'] += int(line[9]) - int(line[6]) + 1
                    elif line[0] == 'TURN':
                        protein['sec_str'] += int(line[8]) - int(line[5]) + 1

                    # atom coordinates
                    elif line[0] == 'ATOM':
                        chain_id = line[4]
                        protein['known_coord'].add(chain_id + line[5])

                        x = float(line[6])
                        y = float(line[7])
                        z = float(line[8])

                        # record min/max coordinates
                        if line[1] == '1':
                            protein['x_min'] = x
                            protein['x_max'] = x
                            protein['y_min'] = y
                            protein['y_max'] = y
                            protein['z_min'] = z
                            protein['z_max'] = z
                        else:
                            if protein['x_min'] > x:
                                protein['x_min'] = x
                            elif protein['x_max'] < x:
                                protein['x_max'] = x
                            if protein['y_min'] > y:
                                protein['y_min'] = y
                            elif protein['y_max'] < y:
                                protein['y_max'] = y
                            if protein['z_min'] > z:
                                protein['z_min'] = z
                            elif protein['z_max'] < z:
                                protein['z_max'] = z

                        # record C_alpha/C_beta coordinates
                        if line[2] == 'CA':
                            if first_CA:
                                first_CA = False
                                protein['x_CA_0'] = x
                                protein['y_CA_0'] = y
                                protein['z_CA_0'] = z
                            protein['x_CA_n'] = x
                            protein['y_CA_n'] = y
                            protein['z_CA_n'] = z
                        elif line[2] == 'CB':
                            if first_CB:
                                first_CB = False
                                protein['x_CB_0'] = x
                                protein['y_CB_0'] = y
                                protein['z_CB_0'] = z
                            protein['x_CB_n'] = x
                            protein['y_CB_n'] = y
                            protein['z_CB_n'] = z

        if args.output is not None:
            img_out = os.path.join(args.output, f'{pdb_id}.png')
            jmol_cmd = f'cartoon only; color cartoon structure; write {img_out} as pngj'
            subprocess.run(['java', '-jar', 'Jmol.jar', pdb_filepath, '-J', jmol_cmd])

    proportion = protein['sec_str'] / len(protein['known_coord'])
    print(f'{pdb_id}\tAnteil AS in Sekundaerstruktur\t{proportion:.4f}')
    dx = protein['x_CA_n'] - protein['x_CA_0']
    dy = protein['y_CA_n'] - protein['y_CA_0']
    dz = protein['z_CA_n'] - protein['z_CA_0']
    print(f'{pdb_id}\tAbstand C_alpha\t{calc_dist(dx, dy, dz):.4f}')
    dx = protein['x_CB_n'] - protein['x_CB_0']
    dy = protein['y_CB_n'] - protein['y_CB_0']
    dz = protein['z_CB_n'] - protein['z_CB_0']
    print(f'{pdb_id}\tAbstand C_beta\t{calc_dist(dx, dy, dz):.4f}')
    dx = protein['x_max'] - protein['x_min']
    dy = protein['y_max'] - protein['y_min']
    dz = protein['z_max'] - protein['z_min']
    print(f'{pdb_id}\tX-Groesse\t{dx:.4f}')
    print(f'{pdb_id}\tY-Groesse\t{dy:.4f}')
    print(f'{pdb_id}\tZ-Groesse\t{dz:.4f}')
    print(f'{pdb_id}\tVolumen\t{dx * dy * dz:.4f}')
