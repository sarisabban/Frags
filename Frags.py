#!/usr/bin/python3

import Bio.PDB , sys
from pyrosetta import *
from pyrosetta.toolbox import *
init()

pose = pose_from_pdb(sys.argv[1])
Vall = sys.argv[2]

def Setup():
	os.system('''
sudo apt install ncbi-blast+
wget http://bioinfadmin.cs.ucl.ac.uk/downloads/psipred/psipred.4.01.tar.gz
tar xzvf psipred.4.01.tar.gz
rm psipred.4.01.tar.gz
cd psipred/src
make
make install

#	which blastp
sed -i 's/set ncbidir = \/usr\/local\/bin/set ncbidir = \/usr\/bin/' runpsipredplus
##### CHANGE the set execdir = /home/acresearch/Desktop/psipred/bin and set datadir = /home/acresearch/Desktop/psipred/data

cd ..
wget ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz
gunzip -v uniref90.fasta.gz
wget http://bioinfadmin.cs.ucl.ac.uk/downloads/pfilt/pfilt1.5.tar.gz
tar xzvf pfilt1.5.tar.gz
rm pfilt1.5.tar.gz
cd pfilt
cc -O pfilt.c -lm -o pfilt
cd ..
pfilt/pfilt uniref90.fasta > uniref90filt
makeblastdb -dbtype 'prot' -in uniref90filt -out uniref90filt
''')

def MakeLocal(pose):
	''' Preforms fragment picking and secondary structure prediction locally '''
	''' Generates the 3-mer file, the 9-mer file, and the PsiPred file '''
	#Generate FASTA file
	sequence = pose.sequence()
	filename = sys.argv[1].split('.')
	fasta = open(filename[0] + '.fasta' , 'w')
	fasta.write(sequence)
	fasta.close()
	#Generate PSIPRED prediction file
#	os.system('./BLAST+/runpsipredplus example/example.fasta')
#	os.rename('.ss2' , 'pre.psipred.ss2')
	#Generate Checkpoint file
#	-in::file::checkpoint .checkpoint
#	os.system('')
	#Generate fragment files
	for frag in [3 , 9]:
		init('-in::file::fasta ' + filename[0] + '.fasta' + ' -in::file::s ' + sys.argv[1] + ' -frags::frag_sizes ' + str(frag) + ' -frags::ss_pred pre.psipred.ss2 predA -frags::n_candidates 1000 -frags:write_ca_coordinates -frags::n_frags 200')
		fregment = pyrosetta.rosetta.protocols.frag_picker.FragmentPicker()
		fregment.parse_command_line()
		fregment.read_vall(Vall)
		fregment.bounded_protocol()
		fregment.save_fragments()
#--------------------------------------------------
#Setup()
MakeLocal(pose)
