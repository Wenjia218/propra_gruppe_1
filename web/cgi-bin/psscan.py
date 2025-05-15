#!/usr/bin/python3
import argparse
import re
import sys
import urllib.request as ul

parser = argparse.ArgumentParser()
parser.add_argument('--fasta', type=str)
parser.add_argument('--pattern')
parser.add_argument('--web', type=str)
parser.add_argument('--extern', action='store_true')
args = parser.parse_args()
fasta = args.fasta

# read fasta and save the sequence in sequences{}
def read_fasta(fasta):
    sequences = {}
    active_sequence_name = ""
    for line in fasta:
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


# translate the pattern and return the match result between the pattern and a sequence
def read_pattern(p):
    pa = p
    pa = pa.strip("<").strip(">")
    pa = pa.replace("-", "")
    pa = pa.replace("x", "[A-Z]")
    pa = pa.replace("{", "[^")
    pa = pa.replace("}", "]")
    pa = pa.replace("(", "{")
    pa = pa.replace(")", "}")
    return pa

# Alternative that fasta could also be read with StdIn
if not fasta == "-":
    with open(fasta, "r") as f:
        sequences = read_fasta(f)
else:
    sequences = read_fasta(sys.stdin)

# if the pattern is empty and the PrositeID is provided, get the pattern of the corresponding ID
if args.pattern:
    pattern = args.pattern
else:
    pattern = ""
    web = args.web
    url = "https://ftp.expasy.org/databases/prosite/prosite.dat"
    ul.urlretrieve(url, "tmp_file.txt")

    with open("tmp_file.txt", 'r') as f:
        ps_id = ""
        for line in f:
            if line.startswith("PA") and ps_id == web:
                pattern += line.split("   ")[1].strip("\n")
                if pattern[-1] == ".":
                    pattern = pattern[:-1]
                    break
            if line.startswith("AC"):
                ps_id = line.split("   ")[1][:-2]

pat = read_pattern(pattern)
re_pattern = re.compile(pat)

# allow multiple sequences
matches = []
for key in sequences:
    for item in re.finditer(re_pattern, sequences[key]):
        matches.append(key + "\t" + str(item.start()) + "\t" + item.group())

for line in matches:
    print(line)