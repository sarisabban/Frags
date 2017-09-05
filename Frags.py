#!/usr/bin/python3

'''
sudo apt install ncbi-blast+
wget http://bioinfadmin.cs.ucl.ac.uk/downloads/psipred/psipred.4.01.tar.gz
tar xzvf psipred.4.01.tar.gz
rm psipred.4.01.tar.gz
cd psipred/src
in ./BLAST+/runpsipredplus change line 17 to (set ncbidir = /usr/bin/psiblast)
make
make install
cd ..
wget ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz
gunzip -v uniref90.fasta.gz


wget http://bioinfadmin.cs.ucl.ac.uk/downloads/pfilt/pfilt1.5.tar.gz
tar xzvf pfilt1.5.tar.gz
rm pfilt1.5.tar.gz
cd pfilt
cc -O pfilt.c -lm -o pfilt
cd ..


pfilt/pfilt uniref90.fasta > uniref90filt						#ERROR HERE:	pfilt not found. Cannot find where the pfilt program is and cannot find from where to install it from
formatdb -t uniref90filt -i uniref90filt						#ERROR HERE:	formatdb not found. Cannot find where the formatdb program is and cannot find from where to install it from
makeblastdb -dbtype prot -in uniref90filt -out uniref90filt				#OK:		Not sure what this does but it works fine
./BLAST+/runpsipredplus example/example.fasta						#ERROR HERE:	/usr/local/bin/psiblast: Command not found. FATAL: Error whilst running blastpgp - script terminated!
'''

import Bio.PDB , sys
from pyrosetta import *
from pyrosetta.toolbox import *
init()

pose = pose_from_pdb(sys.argv[1])
Vall = sys.argv[2]

def MakeLocal(pose):
	''' Preforms fragment picking and secondary structure prediction locally '''
	''' Generates the 3-mer file, the 9-mer file, and the PsiPred file '''
	#Generate FASTA file
	sequence = pose.sequence()
	filename = sys.argv[1].split('.')
	fasta = open(filename[0] + '.fasta' , 'w')
	fasta.write(sequence)
	fasta.close()
	#Generate PSIPRED prediction file (http://bioinfadmin.cs.ucl.ac.uk/downloads/psipred/)
#	os.system('')
#	os.rename('' , 'pre.psipred.ss2')
	#Generate Checkpoint file
#	os.system('')
	#Generate fragment files
	for frag in [3 , 9]:
		init('-in::file::fasta ' + filename[0] + '.fasta' + ' -in::file::s ' + sys.argv[1] + ' -frags::frag_sizes ' + str(frag) + ' -frags::n_candidates 1000 -frags:write_ca_coordinates -frags::n_frags 200')
		fregment = pyrosetta.rosetta.protocols.frag_picker.FragmentPicker()
		fregment.parse_command_line()
		fregment.read_vall(Vall)
		fregment.bounded_protocol()
		fregment.save_fragments()
#--------------------------------------------------
MakeLocal(pose)
