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
        <h2>Prosite-Pattern</h2>
        <form name="psscan" action="s01a07.py" method="post" enctype="multipart/form-data">
            <dl>
                <dt>Fasta File</dt>
                <dd><input type="file" name="fasta" /></dd>
                <dt>Text Input</dt>
                <dd><input type="text" name="in_text" /></dd>
                <dt>Input Type</dt>
                <dd>
                    <input type="radio" id="pattern" name="in_type" value="pattern" />
                    <label for="pattern">Prosite-Pattern</label><br />
                    <input type="radio" id="ps_id" name="in_type" value="ps_id" />
                    <label for="ps_id">ProSiteID</label>
                </dd>
                <dt>External?</dt>
                <dd><input type="checkbox" name="external" value=True /></dd>
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
in_text = form.getvalue('in_text')
in_type = form.getvalue('in_type')
external = False
if form.getvalue('external'):
    external = True
fasta_path = None
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

out = None
if fasta_path is not None:
    command = ['python3', 'cgi-bin/psscan.py', '--fasta', fasta_path]
    if in_type == 'pattern':
        command.append('--pattern')
    elif in_type == 'ps_id':
        command.append('--web')
    command.append(in_text)
    if external:
        command.append('--extern')
    out = subprocess.check_output(command)
    out = out.decode('utf-8', 'ignore')

with open('header.html') as header:
    for line in header:
        print(line)

print(jinja2.Environment().from_string(content).render(result=out))

with open('footer.html') as footer:
    for line in footer:
        print(line)
