# Frags
Generate Fragment Picking and PSIPRED secondary structure prediction.

## Requirements:
1. Make sure you install [PyRosetta](http://www.pyrosetta.org) as the website describes.
2. Use the following command (in GNU/Linux) to install all necessary programs, python libraries, and databases for this script to run successfully (approximately 6 hours to complete):

`python3 Frags.py setup`

3. The vall.jul19.2011.gz database is required to successfully run this script, but the database can only be found in the C++ [Rosetta](https://www.rosettacommons.org) software suite. Unfortunately it is currently not provided with PyRosetta therefore Rosetta needs to be downloaded separately, then uncompressed, to get the database. If you are only interested in getting the database, no need to compile Rosetta if you are not going to use it.

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
