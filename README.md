# Frags
Generate Fragment Picking and PSIPRED secondary structure prediction.

## Requirements:
1. Make sure you install [PyRosetta](http://www.pyrosetta.org) as the website describes.
2. You will also need to install [Rosetta](https://www.rosettacommons.org/) as the website describes.
3. Use the following command (in GNU/Linux) to download the necessary database (NCBI's nr database - 30GB) in the correct directory for this script to run successfully (approximately 3 hours to complete):

`python3 Frags.py setup`

## Description:
This script preforms fragment picking and PSIPRED secondary structure prediction to generate the files required for an Abinitio folding simulation (like the [Robetta](http://www.robetta.org/) server but locally). If you have any comments or problems with the script feel free to email me (sari.sabban@gmail.com).

## How To Use:
1. Use the following command to run the script (approximately 1 hour to complete):

`python3 Frags.py FILENAME.pdb`

2. Output files will be:
* FILENAME.fasta
* frags.200.3mers
* frags.200.9mers
* pre.psipred.ss2
