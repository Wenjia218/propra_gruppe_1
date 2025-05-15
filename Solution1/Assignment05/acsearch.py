#!/usr/bin/env python3

import urllib.request
import argparse as ap

import requests


def swissprot_search():

    # get ac_number from command and parse as variable

    parser = ap.ArgumentParser()
    parser.add_argument('--ac', type=str, required=True)

    args=parser.parse_args()

    ac_number = args.ac

    # download the fasta from uniprot and print

    # url with ac_number

    url = 'https://www.uniprot.org/uniprotkb/'+ ac_number + ".fasta"

    # check if the ac_number exists in uniprot

    try:
        get = requests.get(url)
        if get.status_code == 200:
            with urllib.request.urlopen(url) as f:
                html = f.read().decode('utf-8')
            print(html)

        else:
            print(url + "is not reachable, please try another Ac Number!")

    # show error if is not an existing page:

    except requests.exceptions.RequestException as e:
        raise SystemExit(f"{url}: is not reachable \nErr: {e}")


swissprot_search()