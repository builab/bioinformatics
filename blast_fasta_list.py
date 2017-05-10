# Biopython script to blast from a list of file
# HB 2017/05
 
from Bio.Blast import NCBIWWW
import os

# Function to blast fasta
def blastFasta(fastaFile):
	# Read the fasta file
	fasta_string = open(fastaFile).read()
	name, extension = os.path.splitext(fastaFile)
	xmlFile = name + ".xml"
	# Blast in NCBI
	result_handle = NCBIWWW.qblast("blastp", "refseq_protein", fasta_string)
    # Write out result in xml file
	with open(xmlFile, "w") as out_handle:
		out_handle.write(result_handle.read())
    	
    # Close result	 
	result_handle.close()
	return;
	
# Now start to process the list	
# Parse the list
with open("seq_list_fixed.txt") as f:
	# Loop through each line
	for line in f:
		# Remove white space at the end
		line = line.rstrip('\n')
		# If the string is not empty
		if line:
			print "Blasting UniprotID ", line
			# Blast it
			blastFasta( "fixed_fasta/" + line + ".fasta" )
		
	
