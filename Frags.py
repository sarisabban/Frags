#!/usr/bin/python3
#Authored by Sari Sabban on 7-September-2017 (sari.sabban@gmail.com).

import Bio.PDB , sys
from pyrosetta import *
from pyrosetta.toolbox import *
init()

pose = pose_from_pdb(sys.argv[1])
#-----------------------------------------------------------------------------------------------------
def Setup():
	''' Sets up and installs are the required programs and databases for preforming BLAST+ and PSIPRED calculations '''
	#Install BLAST+
	home = os.getcwd()
	os.system('sudo apt install ncbi-blast+')
	#Download and compile PSIPRED as well as identify important paths
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
	os.system("sed -i 's#set dbname = uniref90filt#" + home + "/psipred/uniref90.fasta#' runpsipredplus")
	os.chdir(home)
	os.chdir('psipred')
	#Download and prepare the Uniref90 database
	os.system('wget ftp://ftp.uniprot.org/pub/databases/uniprot/uniref/uniref90/uniref90.fasta.gz')
	os.system('gunzip -v uniref90.fasta.gz')
	os.system("makeblastdb -in uniref90.fasta -dbtype prot -input_type fasta -out uniref90.fasta")

def MakeLocal(pose):
	''' Preforms fragment picking and secondary structure prediction locally '''
	''' Generates the 3-mer file, the 9-mer file, and the PsiPred file '''
	#Find the Vall Database
	result = []
	for root , dirs , files in os.walk('/'):
		if 'vall.jul19.2011.gz' in files:
			result.append(os.path.join(root))
	Vall = (result[0] + '/')
	#Find the runpsipredplus Executable
	result = []
	for root , dirs , files in os.walk('/'):
		if 'runpsipredplus' in files:
			result.append(os.path.join(root))
	psipredEX = (result[0] + '/')
	#Find the uniref90 Database
	result = []
	for root , dirs , files in os.walk('/'):
		if 'uniref90.fasta' in files:
			result.append(os.path.join(root))
	uniref90 = (result[0] + '/')
	#Generate FASTA file
	sequence = pose.sequence()
	filename = sys.argv[1].split('.')
	fasta = open(filename[0] + '.fasta' , 'w')
	fasta.write(sequence)
	fasta.close()
	#Generate PSIPRED prediction file
	os.system(psipredEX + 'runpsipredplus ' + filename[0] + '.fasta')
	os.rename(filename[0] + '.ss2' , 'pre.psipred.ss2')
	os.remove(filename[0] + '.horiz')
	#Generate Checkpoint file
	os.system('psiblast -db ' + uniref90 + 'uniref90.fasta -query ' + filename[0] + '.fasta')
	os.rename(filename[0] + '.checkpoint' , 'check.checkpoint')
	#Generate fragment files
	for frag in [3 , 9]:
		init('-in::file::fasta ' + filename[0] + '.fasta' + ' -in::file::s ' + sys.argv[1] + ' -frags::frag_sizes ' + str(frag) + ' -frags::ss_pred pre.psipred.ss2 predA -in::file::checkpoint check.checkpoint -frags::n_candidates 1000 -frags:write_ca_coordinates -frags::n_frags 200')
		fregment = pyrosetta.rosetta.protocols.frag_picker.FragmentPicker()
		fregment.parse_command_line()
		fregment.read_vall(Vall + 'vall.jul19.2011.gz')
		fregment.bounded_protocol()
		fregment.save_fragments()
	os.remove('check.checkpoint')
#-----------------------------------------------------------------------------------------------------
#Setup()
MakeLocal(pose)
