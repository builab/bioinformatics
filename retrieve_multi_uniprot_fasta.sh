#/bin/bash
# Biopython Retrieving Seq from Uniprot ID
# Usage: sh retrieve_multi_uniprot_fasta.sh < uniprotID_list.txt
while read uniprotId; do
	echo $uniprotId
	echo curl http://www.uniprot.org/uniprot/${uniprotId}.fasta
	curl http://www.uniprot.org/uniprot/${uniprotId}.fasta > ${uniprotId}.fasta
done

