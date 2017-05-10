#/bin/bash
# Biopython Retrieving Seq from Uniprot ID
uniprotId="I7LY81"

echo curl http://www.uniprot.org/uniprot/${uniprotId}.fasta
curl http://www.uniprot.org/uniprot/${uniprotId}.fasta > ${uniprotId}.fasta