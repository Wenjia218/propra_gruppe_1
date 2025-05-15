#!/usr/bin/python3
# Import modules for CGI handling
import cgi, cgitb
import subprocess
import os

# enable debugging
cgitb.enable()
# print content type
print("Content-type:text/html\n\n")

content = """
    <form name="input" action="s01a06.py" method="get" enctype="multipart/form-data">
        <table>
            <tr>
                <td><input type="file" name="file"/>Choose your file (e.g.swissprot45_head.dat)</td>
                <td><input type="text" name="keywords"/>Please type in keywords of your choice(one or multiple)</td>
            </tr>
        </table>
        <br>
        <br>
        <input style="padding-left: 120px; padding-right: 120px" type="submit" name="submit"/>
    </form>
"""

form = cgi.FieldStorage()
keywords= form.getvalue("keywords")

UPLOAD_DIR = '../uploads'
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
        out = subprocess.check_output(
            ["python3", "../cgi/spkeyword.py", "--swissprot", uploaded_file_path, "--keywords", keywords])
        if out != None:
            out = out.decode('utf-8', 'ignore')


# put header at top for uniform look of website:

with open('header.html') as header:
    for line in header:
        print(line)


print(content)

# put footer at bot for uniform look of website:

with open('footer.html') as footer:
    for line in footer:
        print(line)


