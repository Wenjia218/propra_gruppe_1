#!/usr/bin/python3

import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument('--organism', type=ap.FileType("rt"), required=True)
parser.add_argument('--features', type=ap.FileType("rt"), required=True)

args = parser.parse_args()
organism = args.organism
features = args.features

# read in fasta sequences...
last_ga = ""
genomic_accessions = {}
with open(organism.name) as o:
    for line in o:
        if line[0] == ">":
            last_ga = line.strip(">\n").split(" ")[0]
            genomic_accessions[last_ga] = []
        else:
            genomic_accessions[last_ga].append(line.strip("\n"))

for key in genomic_accessions:
    genomic_accessions[key] = "".join(genomic_accessions[key])

# headers contains indices for cell_content

headers = []
genomic_accession = 0
start = 0
end = 0
locus_tag = 0
with open(features.name) as f:
    i = 0
    for header in f.readline().strip("# \n").split("\t"):
        if header in {"genomic_accession", "start", "end", "strand", "locus_tag"}:
            headers.append(i)
        i += 1
    genomic_accession = headers[0]
    start = headers[1]
    end = headers[2]
    strand = headers[3]
    locus_tag = headers[4]

    for line in f:
        cell_content = line.strip("# \n").split("\t")
        if cell_content[0] == "CDS":
            print(">" + cell_content[locus_tag])
            if cell_content[strand] == "+":
                print(genomic_accessions[cell_content[genomic_accession]][int(cell_content[start]) - 1: int(cell_content[end])])
            else:
                returnval = []
                for char in list(genomic_accessions[cell_content[genomic_accession]][int(cell_content[start]) - 1: int(cell_content[end])][::-1]):
                    if char == 'A':
                        returnval.append('T')

                    elif char == 'T':
                        returnval.append('A')

                    elif char == 'G':
                        returnval.append('C')

                    elif char == 'C':
                        returnval.append('G')
                returnval = "".join(returnval)
                print(returnval)

