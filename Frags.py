#!/usr/bin/python3

import Bio.PDB , sys
from pyrosetta import *
from pyrosetta.toolbox import *
init()

pose = pose_from_pdb(sys.argv[1])

def MakeLocal(pose):
	''' Preforms fragment picking and secondary structure prediction locally '''
	''' Generates the 3-mer file, the 9-mer file, and the PsiPred file '''
	#Generate blueprint file
	filename = 'structure.pdb'
	sslist=list()
	p = Bio.PDB.PDBParser()
	structure = p.get_structure('X', filename)
	model = structure[0]
	dssp = Bio.PDB.DSSP(model, filename)
	for x in dssp:
		if x[2]=='G' or x[2]=='H' or x[2]=='I':
			y = x[1] + ' ' + 'H'
		elif x[2]=='B' or x[2]=='E':
			y= x[1] + ' ' + 'S'
		else:
			y= x[1] + ' ' + 'L'
		sslist.append(y)
	blueprintfile = open('blueprint' , 'w')
	count = 0
	for ss in sslist:
		count += 1
		blueprintfile.write(str(count) + ' ' + ss + '\n')
	blueprintfile.close()
	#Generate FASTA file
	sequence = pose.sequence()
	fasta = open(sys.argv[1] + '.fasta' , 'w')
	fasta.write(sequence)
	fasta.close()
	#Generate PSIPRED prediction file
	psipred = pyrosetta.rosetta.core.io.external.PsiPredInterface(' ')# <------- PROBLEM
	psipred.run_psipred(pose , 'blueprint')# <------- PROBLEM
	os.remove('blueprint')
	#Generate fragment files
	for frag in [3 , 9]:
		init('-in::file::fasta structure.fasta -in::file::s structure.pdb -frags::frag_sizes ' + str(frag) + ' -frags::n_candidates 1000 -frags:write_ca_coordinates -frags::n_frags 200')
		fregment = pyrosetta.rosetta.protocols.frag_picker.FragmentPicker()
		fregment.parse_command_line()
		fregment.read_vall('vall.jul19.2011.gz')
		fregment.bounded_protocol()
		fregment.save_fragments()
#--------------------------------------------------
MakeLocal(pose)
