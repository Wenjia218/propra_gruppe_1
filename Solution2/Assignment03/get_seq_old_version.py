#!/usr/bin/python3
import sys

import pymysql
import argparse as ap


def sequences_to_fasta():
    # ___________________ Argument Parser

    parser = ap.ArgumentParser()

    parser.add_argument('--id', type=str, nargs='+', required=True)
    parser.add_argument('--source', type=str, required=True)
    parser.add_argument('--output', type=ap.FileType("w"), default=sys.stdout)

    args = parser.parse_args()

    searched_key_list = "".join(args.id)  # convert key into string for later seperator deletion
    searched_source = args.source

    # _____________________

    # delete seperator "," of keys and save in list:

    searched_keys = searched_key_list.split(",")

    # get data from data base

    db = pymysql.connect(host="127.0.0.1", user="bioprakt01", passwd="$1$io6mhFO5$MqQTA.eOzVMh2hDdllQij/",
                         database="bioprakt01", port=3308)

    cursor = db.cursor()

    cursor.execute("SELECT * FROM Sequences")  # show all values in Sequences -> perfomance better when not SELECT* TODO

    found_seq = {}  # dictionary for found sequences with key of sequence as key

    for searched_key in searched_keys:
        for row in cursor.fetchall():  # every searched_key and source is compared to key in table and saved if matches

            source = row[0]
            key = row[1]
            seq = row[2]

            if key == searched_key and source == searched_source:
                found_seq[key] = seq

    # print every key with ">" at the front and the sequence in a new line:

    for key, seq in found_seq:
        print(">" + key + "\n" + seq, file=args.output)     #save in a file

    cursor.close()


sequences_to_fasta()
