#!/usr/bin/python3

import cgi
import cgitb
import subprocess

import jinja2

cgitb.enable()

print('Content-type:text/html\r\n\r\n')

content = """
<div id="main">
    <fieldset>
        <h2>Jmol/JSmol Cartoons</h2>
        <form name="visualize_mol" action="s02a09.py" method="get">
        <dl>
            <dt>PDB-ID</dt>
            <dd><input type="text" name="pdb_id" /></dd>
            <dt>Colourize?</dt>
            <dd><input type="checkbox" name="colourized" value=True /></dd>
            <dt>Create .png for Download?</dt>
            <dd><input type="checkbox" name="output" value=True /></dd>
        </dl>
        <input type="submit" value="Submit" />
        </form>
    </fieldset>
    <fieldset>
        {% if result %}
        {{result}}
        {% endif %}
    </fieldset>
</div>
"""

# toggles etc for jsmol widget
# insp https://gist.github.com/jhjensen2/4701339
toggles = """
<dl>
    <dt>Spin</dt>
    <dd>
        <input name="spin" id="spin_on" type="radio" onclick="Jmol.script(jmolApplet0, 'spin on; ');" />
        <label for="spin_on">On</label>
        <input name="spin" id="spin_off" type="radio" onclick="Jmol.script(jmolApplet0, 'spin off; ');" checked="checked" />
        <label for="spin_off">Off</label>
    </dd>
    <dt>Model</dt>
    <dd>
        <input name="model" id="cartoon" type="radio" onclick="Jmol.script(jmolApplet0, 'cartoon only; ');" checked="checked" />
        <label for="cartoon">Cartoon</label>
        <input name="model" id="spacefill" type="radio" onclick="Jmol.script(jmolApplet0, 'spacefill only; ')" />
        <label for="spacefill">Spacefill</label>
        <input name="model" id="trace" type="radio" onclick="Jmol.script(jmolApplet0, 'trace only; ');" />
        <label for="backbone">Trace</label>
        <input name="model" id="wireframe" type="radio" onclick="Jmol.script(jmolApplet0, 'wireframe only; ')" />
        <label for="wireframe">Wireframe</label>
    </dd>
</dl>
"""

form = cgi.FieldStorage()
pdb_id = form.getvalue('pdb_id')
colourized = False
if form.getvalue('colourized'):
    colourized = True
output = False
if form.getvalue('output'):
    output = True

out = None
if pdb_id is not None and len(pdb_id):
    command = ['python3', 'cgi-bin/visualize_mol.py', '--id', pdb_id, '--html']
    if colourized:
        command.append('--colourized')
    if output:
        command.extend(['--output', '.'])
    out = subprocess.check_output(command).decode('utf-8', 'ignore')
    out += toggles

with open('header.html') as header:
    for line in header:
        if line.strip().startswith('</head>'):
            print('\t<script type="text/javascript" src="jsmol/JSmol.min.js"></script>')
            print('\t<script type="text/javascript">')
            print('\t\tconst Info = { width: 500, height: 500, j2sPath: "jsmol/j2s" };')
            print('\t</script>')
        print(line)

print(jinja2.Environment().from_string(content).render(result=out))

with open('footer.html') as footer:
    for line in footer:
        print(line)
