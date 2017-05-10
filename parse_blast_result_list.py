# Biopython: Parse Blast result
# HB 2017/05

from Bio.Blast import NCBIXML
import sys
import os

# Function to parse Blast result
def parseBlastXML(blastXml):
	# Check if this threshold is ok
	E_VALUE_THRESH = 0.04
	name, extension = os.path.splitext(blastXml)
	out = name + ".txt"
	# Write file for output
	f = open(out, 'w')
	# Choose stdout to file
	orig_stdout = sys.stdout
	sys.stdout = f
	# Open result
	result_handle = open(blastXml)
	# Parse Blast Result
	blast_records = NCBIXML.parse(result_handle)
	for blast_record in blast_records:
		for alignment in blast_record.alignments:
			for hsp in alignment.hsps:
				if hsp.expect < E_VALUE_THRESH:
					print('****Alignment****')
					print('sequence:', alignment.title)
					print('length:', alignment.length)
					print('e value:', hsp.expect)
					#print(hsp.query[0:75] + '...')
					#print(hsp.match[0:75] + '...')
					#print(hsp.sbjct[0:75] + '...')
					print("")	
	            
	# Switch back to orig stdout            
	sys.stdout = orig_stdout
	f.close()


# Now start to process the list
with open("seq_list.txt") as f:
	# Loop through each line
	for line in f:
		# Remove white space at the end
		line = line.strip()
		# If the string is not empty
		if line:
			print "Analyzing Blast of UniprotID ", line
			# Parse the blast result
			parseBlastXML( line + ".xml" )
