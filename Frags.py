#!/usr/bin/python3

import Bio.PDB , sys
from pyrosetta import *
from pyrosetta.toolbox import *
init()

pose = pose_from_pdb('structure.pdb')
Vall = '/home/acresearch/rosetta_src_2017.08.59291_bundle/tools/fragment_tools/vall.jul19.2011.gz'

def Setup():
	home = os.getcwd()
	os.system('sudo apt install ncbi-blast+')
	os.system('wget http://bioinfadmin.cs.ucl.ac.uk/downloads/psipred/psipred.4.01.tar.gz')
	os.system('tar xzvf psipred.4.01.tar.gz')
	os.system('rm psipred.4.01.tar.gz')
	os.chdir('psipred/src')
	os.system('make')
	os.system('make install')
	os.chdir(home)
	os.chdir('psipred/BLAST+')
	result = []
	for root , dirs , files in os.walk('/'):
		if 'blastp' in files:
			result.append(os.path.join(root))
	directory = (result[0] + '/')
	os.system("sed -i 's#/usr/local/bin#'" + directory + "# runpsipredplus")
	os.system("sed -i 's#set execdir = ../bin#set execdir = " + home + "/psipred/bin#' runpsipredplus")
	os.system("sed -i 's#set datadir = ../data#set datadir = " + home + "/psipred/data#' runpsipredplus")
	os.chdir(home)
	os.chdir('psipred')
	os.system('wget http://bioinfadmin.cs.ucl.ac.uk/downloads/pfilt/pfilt1.5.tar.gz')
	os.system('tar xzvf pfilt1.5.tar.gz')
	os.system('rm pfilt1.5.tar.gz')
	os.system('cc -O pfilt/pfilt.c -lm -o pfilt/pfilt')
	os.system('wget ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz')
	os.system('gunzip -v uniref90.fasta.gz')
	os.system('pfilt/pfilt uniref90.fasta > uniref90filt')
	os.system('makeblastdb -dbtype 'prot' -in uniref90filt -out uniref90filt')

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
Setup()
#MakeLocal(pose)
