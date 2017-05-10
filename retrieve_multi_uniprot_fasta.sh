#/bin/bash
# Biopython Retrieving Seq from Uniprot ID

while read uniprotId; do
	echo $uniprotId
	echo curl http://www.uniprot.org/uniprot/${uniprotId}.fasta
	curl http://www.uniprot.org/uniprot/${uniprotId}.fasta > ${uniprotId}.fasta
done < seq_list_fixed.txt

