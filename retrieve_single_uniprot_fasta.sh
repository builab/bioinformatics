#/bin/bash
# Biopython Retrieving Seq from Uniprot ID
uniprotId="I7LY81"

echo curl https://www.uniprot.org/uniprot/${uniprotId}.fasta
curl https://www.uniprot.org/uniprot/${uniprotId}.fasta > ${uniprotId}.fasta
