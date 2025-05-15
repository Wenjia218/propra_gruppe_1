#!/usr/bin/python3
# Import modules for CGI handling
import cgi, cgitb
import subprocess
import os

# enable debugging
import jinja2

cgitb.enable()
# print content type
print("Content-type:text/html\n\n")

content = """
<div id="main">
<fieldset>
    <h2>Swissprot-Keyword</h2>
    <form name="input" action="s01a06.py" method="post" enctype="multipart/form-data">
        <dl>
            <dt>File</dt>
            <dd><input type="file" name="file"/></dd>
            <dt>Keywords</dt>
            <dd><input type="text" name="keywords"/></dd>
        </dl>
        <input type="submit" value="Submit"/>
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
keywords= form.getvalue("keywords")

UPLOAD_DIR = './uploads'
out = None



if "file" in form:
    form_file = form['file']
    if form_file.filename:
        uploaded_file_path = os.path.join(UPLOAD_DIR, os.path.basename(form_file.filename))
        with open(uploaded_file_path, 'wb') as fout:
            while True:
                chunk = form_file.file.read(10000)
                if not chunk:
                    break
                fout.write(chunk)
        command = f'python3 cgi-bin/spkeyword.py --swissprot {uploaded_file_path} --keywords {keywords}'.split(';')
        out = subprocess.check_output(command)
        if out != None:
            out = out.decode('utf-8', 'ignore')


# put header at top for uniform look of website:

with open('header.html') as header:
    for line in header:
        print(line)


print(jinja2.Environment().from_string(content).render(result=out))

# put footer at bot for uniform look of website :

with open('footer.html') as footer:
    for line in footer:
        print(line)


