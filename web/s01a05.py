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
        <h2>Swissprot Search</h2>
        <form name="acsearch" action="s01a05.py" method="get">
            <dl>
                <dt>Accession Nr.</dt>
                <dd><input type="text" name="seqid" /></dd>
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
seqid = form.getvalue('seqid')
out = None
if seqid is not None and len(seqid):
    out = subprocess.check_output(f'python3 ./cgi-bin/acsearch.py --ac {seqid}'.split(' '))
    out = out.decode('utf-8', 'ignore')

with open('header.html') as header:
    for line in header:
        print(line)

print(jinja2.Environment().from_string(content).render(result=out))

with open('footer.html') as footer:
    for line in footer:
        print(line)
