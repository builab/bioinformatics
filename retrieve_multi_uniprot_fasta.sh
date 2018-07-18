#/bin/bash
# Biopython Retrieving Seq from Uniprot ID
# Usage: sh retrieve_multi_uniprot_fasta.sh < uniprotID_list.txt
while read uniprotId; do
	echo $uniprotId
	echo curl https://www.uniprot.org/uniprot/${uniprotId}.fasta
	curl https://www.uniprot.org/uniprot/${uniprotId}.fasta > ${uniprotId}.fasta
done

