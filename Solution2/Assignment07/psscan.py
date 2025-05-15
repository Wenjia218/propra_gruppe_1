#!/usr/bin/python3
import argparse
import re
import sys
import urllib.request as ul
import pymysql

parser = argparse.ArgumentParser()
parser.add_argument('--fasta', type=str)
parser.add_argument('--db', action='store_true')
parser.add_argument('--pattern')
parser.add_argument('--web', type=str)
parser.add_argument('--extern', action='store_true')
args = parser.parse_args()

db = pymysql.connect(host="127.0.0.1", port=3307, database="bioprakt01", user="bioprakt01", password="$1$io6mhFO5$MqQTA.eOzVMh2hDdllQij/")
cursor = db.cursor()

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


# if a fasta file is provided
if_db = False
if args.fasta:
    fasta = args.fasta
    # Alternative that fasta could also be read with StdIn
    if not fasta == "-":
        with open(fasta, "r") as f:
            sequences = read_fasta(f)
    else:
        sequences = read_fasta(sys.stdin)
# find sequence in DB
else:
    if_db = True
    sql = "SELECT ID, Sequence FROM Sequences WHERE"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for seq in results:
            sequences = {}
            sequences.update({seq[0]: seq[1]})
    except:
        print("Error: unable to fetch data")
    db.close()

# if the pattern is empty and the ProSiteID is provided, get the pattern from the corresponding ID
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
    if not if_db:
        for item in re.finditer(re_pattern, sequences[key]):
            matches.append(key + "\t" + str(item.start()) + "\t" + item.group())
    else:
        for item in re.finditer(re_pattern, sequences[key]):
            matches.append(key + "\t" + item.group())

for line in matches:
    print(line)
