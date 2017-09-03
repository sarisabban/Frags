# Frags
Generate Fragment Picking and PSIPRED secondary structure prediction.

## Requirements:
1. Make sure you install [PyRosetta](http://www.pyrosetta.org) as the website describes.
2. Use the following command (in GNU/Linux) to install all necessary Python libraries for this script to run successfully:

`sudo apt install python3-pip && sudo python3 -m pip install biopython`

3. The vall.jul19.2011.gz database is required to successfully run this script, the database can be found in the C++ [Rosetta](https://www.rosettacommons.org) software suite at path `{ROSETTA}/tools/fragment_tools/`, unfortunately it is currently not provided with PyRosetta therefore Rosetta needs to be downloaded separately,then uncompressed, to get the database. If you are only interested in getting the database, no need to compile Rosetta if you are not going to use it.

## Description:
This script preforms fragment picking and PSIPRED secondary structure prediction to generate the files required for an Abinitio folding simulation (like the [Robetta](http://www.robetta.org/) server but locally).

## How To Use:
1. Make sure the vall.jul19.2011.gz is in the local directory (or point to its path from within the script - line 48)
2. Use the following command to run the script:

`python3 Frags.py FILENAME.pdb`

3. Output files will be:
* FILENAME.fasta
* frags.200.3mers
* frags.200.9mers
* prediction.psipred.ss2
