# Biopython script to blast from a list of file
# HB 2017/05
# Update 2020/02
 
from Bio.Blast import NCBIWWW
import os
import sys

tetra="txid5911[ORGN]"
homosapien="txid9606[ORGN]"
chlamy="txid3052[ORGN]"


# Function to blast fasta
def blastFasta(fastaFile):
	# Read the fasta file
	fasta_string = open(fastaFile).read()
	name, extension = os.path.splitext(fastaFile)
	xmlFile = name + ".xml"
	# Blast in NCBI
	result_handle = NCBIWWW.qblast("blastp", "refseq_protein", fasta_string, entrez_query=tetra)
    # Write out result in xml file
	with open(xmlFile, "w") as out_handle:
		out_handle.write(result_handle.read())
    	
    # Close result	 
	result_handle.close()
	return;
	
# Now start to process the list	
# Parse the list
with open(sys.argv[0]) as f:
	# Loop through each line
	for line in f:
		# Remove white space at the end
		line = line.strip()
		# If the string is not empty
		if line:
			print "Blasting UniprotID ", line
			# Blast it
			blastFasta( line + ".fasta" )
		
	
