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
        <h2>Genome Report</h2>
        <form name="genome_length" action="s01a08.py" method="get">
            <dl>
                <dt>RegEx</dt>
                <dd><input type="text" name="regexps" /><br />
                <small>Separate multiple regular expressions with SPACE.</small></dd>
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
regexps = form.getvalue('regexps')
out = None
if regexps is not None and len(regexps):
    out = subprocess.check_output(f'python3 ./cgi-bin/genome_length.py --organism {regexps}'.split(' '))
    out = out.decode('utf-8', 'ignore')

with open('header.html') as header:
    for line in header:
        print(line)

print(jinja2.Environment().from_string(content).render(result=out))

with open('footer.html') as footer:
    for line in footer:
        print(line)
