#!/usr/bin/python3

import argparse
import os.path
import pathlib
import subprocess
import sys
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--id', type=str, help='PDB-ID', default=sys.stdin)
parser.add_argument('--output', type=pathlib.Path)
parser.add_argument('--html', action='store_true', help='use JSmol instead', default=False)
# what is this mix of BE and AE. why is this.
parser.add_argument('--colourized', action='store_true', help='colorize the secondary structures', default=False)
args = parser.parse_args()

url = f'https://files.rcsb.org/download/{args.id}.pdb'
with urllib.request.urlopen(url) as response:
    data = response.read().decode('utf-8', 'ignore')
    if data is not None and len(data):
        tmp_pdb = os.path.join('tmp', f'{args.id}.pdb')
        with open(tmp_pdb, 'wt') as f:
            for line in data:
                f.write(line)

        jmol_cmd = ['cartoon only']
        if args.colourized:
            jmol_cmd.append('color structure')
        out_file = None
        if args.output is not None:
            out_file = f'{args.id}.png'
            if not args.html:
                out_file = os.path.join(args.output, out_file)
            jmol_cmd.append(f'write {out_file} as pngj')
        jmol_cmd = '; '.join(jmol_cmd)

        if args.html:
            print()
            print('<script type="text/javascript">')
            print('\tjmolApplet0 = Jmol.getApplet("jmolApplet0", Info);')
            print(f'\tJmol.script(jmolApplet0, "load {tmp_pdb}; {jmol_cmd}");')
            print('</script>')
            print()
        else:
            subprocess.run(['java', '-jar', 'Jmol.jar', tmp_pdb, '-J', jmol_cmd])
