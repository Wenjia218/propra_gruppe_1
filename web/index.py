#!/usr/bin/python3

import cgi
import cgitb

cgitb.enable()

print('Content-type:text/html\r\n\r\n')

content = """
<div id="main">
    <fieldset>
        <h2>Index / About</h2>
        <dl>
            <dt>Group Members</dt>
            <dd>Julia Folwark, Adrian H&ouml;lzlwimmer, Yin Lei, Wenjia Zhong</dd>
            <dt>Group Number</dt>
            <dd>01</dd>
            <dt>Coaches / Supervisors</dt>
            <dd>Volker Heun, Markus Joppich, Samuel Klein</dd>
        </dl>
    </fieldset>
</div>
"""

with open('header.html') as header:
    for line in header:
        print(line)

print(content)

with open('footer.html') as footer:
    for line in footer:
        print(line)
