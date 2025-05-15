#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('genomes', action='extend', nargs='+', type=argparse.FileType('rt'), help='file(s) w/ genome')
args = parser.parse_args()

nucleotides = ['A', 'C', 'G', 'T']
sequences = ['CTAG', 'CG', 'AACCCTGTC', 'ATG']

with open('results.txt', 'wt') as results:
    for gen_path in args.genomes:
        with open(gen_path.name) as gen_file:
            organism = ''
            genome = ''
            for line in gen_file:
                if line.startswith('>'):
                    if 0 <= line.find('tuberculosis'):
                        organism = 'Mycobacterium tuberculosis'
                    else:
                        organism = 'Mensch, Chromosom 8'
                else:
                    genome += line.strip()
            genome = genome.upper()

            # determine nucleotide frequencies
            nu_freq = {}
            for nucleotide in nucleotides:
                nu_freq[nucleotide] = genome.count(nucleotide) / len(genome)

            incidences = []
            for sequence in sequences:
                # expected value using p = 1/4
                exp_uniform = 0.25 ** len(sequence) * (len(genome) - len(sequence))
                # expected value using relative frequencies
                p = 1
                for base in sequence:
                    p *= nu_freq[base]
                exp_relative = p * (len(genome) - len(sequence))
                # actual incidences
                inc = genome.count(sequence)
                # fold change
                fc = inc / exp_relative

                incidences.append({
                    'sequence': sequence,
                    'exp_uniform': exp_uniform,
                    'exp_relative': exp_relative,
                    'inc': inc,
                    'fc': fc
                })

            results.write(f'{organism}\n\n')

            results.write(f'A: {nu_freq["A"] * 100: .2f}%\t')
            results.write(f'C: {nu_freq["C"] * 100: .2f}%\t')
            results.write(f'G: {nu_freq["G"] * 100: .2f}%\t')
            results.write(f'T: {nu_freq["T"] * 100: .2f}%\n\n')

            for incidence in incidences:
                results.write(f'{incidence["sequence"]}:\t')
                results.write(f'{incidence["exp_uniform"]: .0f}\t')
                results.write(f'{incidence["exp_relative"]: .0f}\t')
                results.write(f'{incidence["inc"]}\t')
                results.write(f'{incidence["fc"]: .1f}\n')

            results.write('\n\n')
