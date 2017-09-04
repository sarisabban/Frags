#!/usr/bin/python3

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
	#Generate Checkpoint file (ftp://ftp.ncbi.nih.gov/blast/executables/blast+/LATEST/)
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
