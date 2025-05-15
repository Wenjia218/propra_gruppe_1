#!/usr/bin/python3

import cgi
import cgitb
import os.path
import subprocess

import jinja2

cgitb.enable()

print('Content-type:text/html\r\n\r\n')

content = """
<div id="main">
    <fieldset>
        <h2>DNA2RNA</h2>
        <form name="dna2rna" action="s01a10.py" method="post" enctype="multipart/form-data">
            <dl>
                <dt>Transformation</dt>
                <dd>
                    <input type="radio" id="genome2orf" name="transformation" value="genome2orf" />
                    <label for="genome2orf">Genome to ORF</label><br />
                    <input type="radio" id="dna2mrna" name="transformation" value="dna2mrna" />
                    <label for="dna2mrna">DNA to mRNA</label><br />
                    <input type="radio" id="mrna2aa" name="transformation" value="mrna2aa" />
                    <label for="mrna2aa">mRNA to amino acids</label>
                </dd>
                <dt>Fasta File</dt>
                <dd><input type="file" name="fasta" /><br />
                <small>Required</small></dd>
                <dt>Feature Table</dt>
                <dd><input type="file" name="features" /><br />
                <small>Only necessary for <q>Genome to ORF</q></small></dd>
            </dl>
            <input type="submit" value="Submit" />
        </form>
    </fieldset>
    <fieldset>
        {% if result %}
        <pre>{{result}}</pre>
        {% endif %}
    </fieldset>
</div>
"""

form = cgi.FieldStorage()
transformation = form.getvalue('transformation')
fasta_path = None
features_path = None
if 'fasta' in form:
    fasta_file = form['fasta']
    if fasta_file.filename:
        fasta_path = os.path.join('uploads', fasta_file.filename)
        with open(fasta_path, 'wb') as fasta_out:
            while True:
                chunk = fasta_file.file.read(100_000)
                if not chunk:
                    break
                fasta_out.write(chunk)
if transformation == 'genome2orf' and 'features' in form:
    features_file = form['features']
    if features_file.filename:
        features_path = os.path.join('uploads', features_file.filename)
        with open(features_path, 'wb') as features_out:
            while True:
                chunk = features_file.file.read(100_000)
                if not chunk:
                    break
                features_out.write(chunk)

out = None
if fasta_path is not None and (features_path is not None or not transformation == 'genome2orf'):
    command = ''
    if transformation == 'genome2orf':
        command = f'python3 cgi-bin/genome2orf.py --organism {fasta_path} --features {features_path}'.split(' ')
    elif transformation == 'dna2mrna':
        command = f'python3 cgi-bin/dna2mrna.py --fasta {fasta_path}'.split(' ')
    elif transformation == 'mrna2aa':
        command = f'python3 cgi-bin/mrna2aa.py --fasta {fasta_path}'.split(' ')
    if len(command):
        out = subprocess.check_output(command)
        out = out.decode('utf-8', 'ignore')

with open('header.html') as header:
    for line in header:
        print(line)

print(jinja2.Environment().from_string(content).render(result=out))

with open('footer.html') as footer:
    for line in footer:
        print(line)
