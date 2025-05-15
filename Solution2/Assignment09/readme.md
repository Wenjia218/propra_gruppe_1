# How to Use JMol

## Installation & Setup

Follow the instructions for how to [download Jmol](https://jmol.sourceforge.net/download/).

1.  Download the `.zip` from [Jmol Files](https://sourceforge.net/projects/jmol/files/).
2.  Unzip the download.
3.  Open the `Jmol.jar`.

## Generate Molecule Structures

There are multiple ways to have Jmol generate molecule structures, most of which are accessible through the File menu in the Jmol window or with right-click.

- Open a `.pdb` file, like one you may have gotten by using the `get_pdb.py` script.
  - The folder icon in the symbol bar also does this.
  - You can use `java -jar Jmol.jar [filename]` in the command line to the same effect.
- Enter a URL of a molecule model, for instance `https://files.rcsb.org/download/4hhb.pdb`
- Directly use a PDB-ID, like `11as`
- Use the MOL option to directly enter molecules. Some examples:
  - Molecule name: `cholesterol`
  - SMILES: `OC[C@@H](O1)[C@@H](O)[C@H](O)[C@@H](O)[C@H](O)1`
  - Standard InCHI: `InChI=1S/C6H8O6/c7-1-2(8)5-3(9)4(10)6(11)12-5/h2,5,7-10H,1H2/t2-,5+/m0/s1`
  - InChIKey: `BQJCRHHNABKAKU-KBQPJGBKSA-N`
  - CAS Registry Number: `58-08-2`

## Console & Commands

You can modify the appearance of the molecules by selecting various options in the menu that shows up when you right click on the image, or through script commands.
The script commands can be entered through the Jmol console, through a `.spt` script file, or as a command line parameter when opening Jmol.

When using the command line, the structure goes like so, in this order:
`java -jar Jmol.jar [file.pdb] [-J "commands"] [-s file.spt] [-j "commands"]`
(either part in brackets is optional)

Most of the commands here will take [atom expressions](https://chemapps.stolaf.edu/jmol/docs/#atomexpressions) as arguments, to specify which collection of atoms are addressed.

The final `;` is optional.

### Display

You can apply different styles to display the molecule as; most of these can be `on` or `off` or a specific value or `only`:

- `spacefill 100%;` or `spacefill on` or `spacefill only` (spheres/spacefill)
- `wireframe 0.15; spacefill 23%;` (ball-and-stick)
- `wireframe 0.3; spacefill off;` (stick model)
- `wireframe 0.01; spacefill 0;` or `wireframe on; spacefill off;` or `wireframe only` (wireframe)
- `select protein, nucleic; cartoon only; color cartoon structure;` (macromolecules as cartoon)
- `isosurface solvent;` or `isosurface molecular;` (cloud effect)
- `trace on;` (emphasise backbone)
- `ribbon on;` (continuous ribbon through the backbone)

The comand to change the colors is `color [object] [color]` where the `[object]` is optional and `[color]` may be a specific color or set to `CPK` for the default coloring.

You can add labels:

- `label{s} %m` (one-letter amino acid for current selection)
- `label{s} %n` (three-letter amino acids for current selection)
- `label{s} %r` (residue number for current selection)

Use `display within([dist], [ref]);` to show atoms based on distances.

Specific kinds of bonds can also be toggled:

- `h-bond{x}` can be `on` or `off` or a specific value (default coloring is green)
- `ssbond{x}` has the same options, and is gold by default

### Select

You can select various parts of a molecule structure and modify them.
For the use with `.pdb` files, these options seem particularly interesting:

- `select protein;`, `select amino;`
- `select [three-letter amino acid code];`
- `select [start]-[end];`
- `select helix;`, `select sheet;`
- `select all;`, `select *;`

You can select multiple things in one command, like `select helix, sheet;` or `select asp, glu;`

For other purposes, these may also be interesting:

- `select dna;`, `select rna;`, `select nucleic;`

### Save as .png

You can use the camera icon in the symbol bar, or open the File menu and select Export from there.

Using the script commands in Jmol, you can use `write image pngj [PDB-ID].png;` or `write [PDB-ID].png as pngj;` to save the structure as an image that Jmol can open again as a 3D structure.

## Command Line Examples

You should be able to run this command from this directory:
`java -jar Jmol.jar 4hhb.pdb -J "select protein; cartoon only; color cartoon structure; write 4hhb.png as pngj;"`

Using the Python script in this directory:
`python3 visualize_mol.py 1crn`
optionally with `--output .` and/or `--colourized`;
you'll need to manually close Jmol or interrupt the process though.

## Further Reading

[Jmol Wiki](https://wiki.jmol.org)

[Script Command Quick Reference Guide](https://biosci.mcdb.ucsb.edu/biochemistry/info/scriptguide.htm)

[Jmol/JSmol Interactive Script Documentation](https://chemapps.stolaf.edu/jmol/docs/)