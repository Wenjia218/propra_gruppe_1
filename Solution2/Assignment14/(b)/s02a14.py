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
        <h2>HOMSTRAD</h2>
        <form name="homstrad" action="s02a14.py" method="post" enctype="multipart/form-data">
            <dl>
                <dt>Text Input</dt>
                <dd><input type="text" name="in_text" /></dd>
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

in_text = None
form = cgi.FieldStorage()
in_text = form.getvalue('in_text')
command = ['python3', 'cgi-bin/web_homstrad.py', '--id', in_text]
out = None

if in_text is not None:
    out = subprocess.check_output(command)
    out = out.decode('utf-8', 'ignore')

with open('header.html') as header:
    for line in header:
        print(line)

print(jinja2.Environment().from_string(content).render(result=out))

with open('footer.html') as footer:
    for line in footer:
        print(line)
