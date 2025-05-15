#!/usr/bin/python3.10

import argparse as ap

parser = ap.ArgumentParser()
parser.add_argument('--fasta', type=ap.FileType("rt"))

args = parser.parse_args()
fasta = args.fasta

triplet_dict = {"GCG" :"A","GCA" :"A","GCU" :"A","GCC" :"A",
   "AGG" :"R","AGA" :"R","CGG" :"R", "CGA" :"R","CGU" :"R","CGC" :"R",
   "AAU" :"N","AAC" :"N",
   "GAU" :"D", "GAC":"D", "UGU" :"C","UGC" :"C",
   "CAG" :"Q","CAA" :"Q",
   "GAG" :"E","GAA" :"E",
   "GGG" :"G","GGA" :"G","GGU" :"G","GGC" :"G",
   "CAU" :"H","CAC" :"H",
   "AUA" :"I","AUU" :"I","AUC" :"I",
   "UUG" :"L","UUA" :"L","CUG" : "L","CUA" :"L","CUU" :"L","CUC" :"L",
   "AAG" :"K","AAA" :"K",
   "UGU" :"C","UGC" :"C",
   "AUG" :"M" ,
   "UUU" :"F" ,"UUC" :"F" ,
   "CCG" :"P" ,"CCA" :"P" ,"CCU" :"P" ,"CCC" :"P" ,
   "AGU" :"S" ,"AGC" :"S" ,"UCG" :"S" ,"UCA" :"S" ,"UCU" :"S" ,"UCC" :"S" ,
   "ACG" :"T" ,"ACA" :"T" ,"ACU" :"T" ,"ACC" :"T" ,
   "UGG" :"W" ,
   "UAU" :"Y" ,"UAC" :"Y" ,
   "GUG" :"V" ,"GUA" :"V" ,"GUU" :"V" ,"GUC" :"V",
   "UAA" :"", "UGA" :"", "UAG": ""
}

def join_string(charlist):
    if len(charlist) % 3 > 0:
        return ""
    index = 0
    aminoacids = []
    while index < len(charlist):
        triplet = "".join(charlist[index:index+3])
        if not (triplet in triplet_dict.keys()):
            return ""
        elif triplet in {"UAA", "UGA", "UAG"}:
            print_string = "".join(aminoacids)
            return print_string
        else:
            aminoacids.append(triplet_dict[triplet])

        index += 3

    print_string = "".join(aminoacids)
    return print_string





char_list = []
head = ""
for line in args.fasta:
    if line[0] == ">":
        sequence = join_string(char_list).strip()
        if not sequence == "":
            print(head + sequence)
        head = line.split(" ")[0]
        char_list = []
    else:
        char_list.extend(line.strip())
sequence = join_string(char_list).strip()
if not sequence == "":
    print(head + sequence)