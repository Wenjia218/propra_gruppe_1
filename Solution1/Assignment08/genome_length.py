#!/usr/bin/env python3
import re
import urllib.request
import argparse as ap
import os
from collections import defaultdict

import requests


def genome_report():
    parser = ap.ArgumentParser()
    parser.add_argument('--organism', type=str, nargs="+", required=True)

    args = parser.parse_args()

    regular_exp = args.organism

    url = "ftp://ftp.ncbi.nlm.nih.gov/genomes/GENOME_REPORTS/prokaryotes.txt"

    genome_file = "test.txt"  # path of saved file

    with open(genome_file, 'w') as f:
        f.write("")

    urllib.request.urlretrieve(url,genome_file) # instead of saving just read every line

    matching_genomes = defaultdict(lambda: 0)       # ordered dictionary for results

    # go through every line of file

    # at position 7 is size of genome
    # at position 1 is name
    # at position 16 is status      of splitted_line

    file = open(genome_file, encoding="utf-8")          # is not being closed anymore -> can be inefficient
    for line in file:
        splitted_line = line.split("\t")
        genome_name = splitted_line[0]

        for pattern in regular_exp:     # match every regular expression that was input
            if re.match(pattern, genome_name) and splitted_line[15] == "Complete Genome":
                print(genome_name + "\t" + splitted_line[6])        # print all names with length


genome_report()
