#!/usr/bin/python3.10

import argparse
import os.path
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('--input', type=argparse.FileType('rt'), help='path to encode.csv file', required=True)
parser.add_argument('--output', type=pathlib.Path, help='path to output directory', required=True)
args = parser.parse_args()

if not os.path.isdir(args.output):
    print('The given output path is not an existing directory! Please retry with an existing directory.')

else:
    first_line = True
    keys = []
    encode = []
    exptypes = {}
    antibodies = {}
    chip_rna_seq = {}

    for line in args.input:
        if first_line:
            first_line = False
            keys = line.strip().split(',')

        else:
            # turn data from encode.csv into list of dict items
            # (this might not actually be necessary for this task)
            values = line.strip().split(',')
            experiment = {}
            for i in range(len(keys)):
                experiment[keys[i]] = values[i]
            encode.append(experiment)

            # count different Data_Type uses
            if experiment['Data_Type'] not in exptypes.keys():
                exptypes[experiment['Data_Type']] = 1
            else:
                exptypes[experiment['Data_Type']] += 1

            # collect Cell_Type uses and their antibodies if ChIP-seq
            antibody = ''
            if experiment['Cell_Type'] not in antibodies.keys():
                antibodies[experiment['Cell_Type']] = set()
            if experiment['Data_Type'] == 'ChIP-seq' and experiment['Experimental_Factors'].startswith('Antibody='):
                antibody = experiment['Experimental_Factors'].split(' ')[0].split('=')[1]
                antibodies[experiment['Cell_Type']].add(antibody)

            # collect DCC_Accession of ChIP-seq with Antibody=H3K27me3
            if experiment['Data_Type'] == 'ChIP-seq' and antibody == 'H3K27me3':
                if experiment['Cell_Type'] not in chip_rna_seq.keys():
                    chip_rna_seq[experiment['Cell_Type']] = {'chip': [], 'rna': []}
                if 0 < len(experiment['DCC_Accession']):
                    chip_rna_seq[experiment['Cell_Type']]['chip'].append(experiment['DCC_Accession'])
            # collect DCC_Accession of RNA-seq with same Cell_Type as the ones above
            if experiment['Data_Type'] == 'RNA-seq' and experiment['Cell_Type'] in chip_rna_seq.keys():
                if 0 < len(experiment['DCC_Accession']):
                    chip_rna_seq[experiment['Cell_Type']]['rna'].append(experiment['DCC_Accession'])

    # write output files
    with open(os.path.join(args.output, 'exptypes.tsv'), 'wt') as exp_file:
        for (exptype, count) in exptypes.items():
            exp_file.write(exptype + '\t' + str(count) + '\n')

    with open(os.path.join(args.output, 'antibodies.tsv'), 'wt') as anti_file:
        for (cell_type, antibody_set) in antibodies.items():
            anti_file.write(cell_type + '\t' + str(len(antibody_set)) + '\n')

    with open(os.path.join(args.output, 'chip_rna_seq.tsv'), 'wt') as chip_rna_file:
        chip_rna_file.write('cell line\tRNAseq Accession\tChIPseq Accession\n')
        for (cell_type, accessions) in chip_rna_seq.items():
            if 0 < len(accessions['rna']):
                accessions['rna'].sort()
                accessions['chip'].sort()
                chip_rna_file.write(cell_type + '\t')
                chip_rna_file.write(','.join(accessions['rna']) + '\t')
                chip_rna_file.write(','.join(accessions['chip']) + '\n')
