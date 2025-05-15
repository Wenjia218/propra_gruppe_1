This folder is meant for everything to do the web page parts,
with the scripts building the actual pages directly in here,
and the scripts to run for the actual work in the `/cgi-bin` folder.
There are separate folders for `/uploads` and `/outputs`, should they be necessary.

When a new page building script is added,
a link should also be added in `header.txt`.

Before uploading, make sure that all files in the `/web` and `/cgi-bin` folders use the `LF` setting for line separators.
You can do this in PyCharm by selecting the `propra_gruppe_1` at the root
(or for this specifically selecting the `/web` folder is also enough)
and open this menu:
> `File` > `File Properties` > `Line Separators` > `LF - Unix and macOS (\n)`

To send all the files and folders to your `public_html` folder, you can use this command
(after navigating to this `/web` folder locally):  
> Linux: `scp -r -P 12 ./* [CIP-handle]@bioclient1.bio.ifi.lmu.de:~/public_html/`  
> Windows: `scp -r -P 12 .\* [CIP-handle]@bioclient1.bio.ifi.lmu.de:~/public_html/`

Once it's up, you should log in via ssh and update the permissions, like so:  
> `ssh -p12 [CIP-handle]@bioclient1.bio.ifi.lmu.de`  
> `cd public_html`  
> `chmod 755 *.py`

If everything worked correctly, you should be able to visit the resulting pages by clicking through from `http://bioclient1.bio.ifi.lmu.de/~[CIP-handle]/index.py`
(if you're connected via eduVPN already)

For debugging, use this command to access the error log after logging in on bioclient1:
> `tail -f /var/log/apache2/error_log`