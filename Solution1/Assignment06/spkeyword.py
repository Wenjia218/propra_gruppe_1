#!/usr/bin/env python3

import argparse as ap
from collections import defaultdict, OrderedDict
import re


def keyword_search():

    # get keyword and file input from command and parse as variable in keywords

    parser = ap.ArgumentParser()
    parser.add_argument('--keywords', type=str,nargs='+', required=True)    # nargs for allowing multiple keywords
    parser.add_argument('--swissprot', type=str, required= True)

    args = parser.parse_args()

    user_keywords = args.keywords     # strip for matching, take multiple keywords and join
    swissprot_file = args.swissprot

    # read swissprot file and extract distinct AC number with the corresponding keyword

    allEntries = defaultdict(lambda:0)      #defaultdict for ordered dictionary with entries from file

    with open(swissprot_file, 'r') as swissprot:
        # only look at lines that start with AC or KW, for performance

        ac_value = ""   # strings to save the found lines in dictionary
        kw_value = ""

        for line in swissprot:
            if line.startswith("AC"):
                line = line[2:]
                ac_value += line.replace("\n","").replace(".","")   # delete all unnecessary characters

            if line.startswith("KW"):
                line = line[2:]
                kw_value += line.replace("\n","").replace(".","")

            if line.startswith("//"):       # at the end of entry reset values in order to not have KW from previous
                if ac_value != "":          # deleting all entries without AC
                    allEntries[ac_value] = kw_value
                    ac_value = ""
                    kw_value = ""



    results = []         # resulting AC numbers

    # go through dictionary and check if keyword is in the values
    for key,value in allEntries.items():
        line = str(value).split(";")
        is_matching = False     # shows if there was a match

        for keyword in user_keywords:       # check for every keyword from user
            for words in line:
                word = words.strip()
                if(word == keyword.strip()):   # checks if string is identical
                    is_matching = True

        if is_matching is True:
            if len(key) != 0:   # in order to skip entries without AC number
                ac_number = str(key).strip().split(";")     # take key from matching keywords and split for multiple AC numbers
                ac_number = ac_number[:-1] # in order to remove "" elements after splitting with ";"
                stripped = [n.strip() for n in ac_number]       # remove whitespace in order to sort
                for element in stripped:
                    results.append(element)

    if results: # in order to avoid printing newline, when empty
        print(*sorted(list(dict.fromkeys(results))),sep="\n") # sort all the numbers in lexicographical order and remove duplicates

keyword_search()