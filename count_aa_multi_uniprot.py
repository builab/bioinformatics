# Biopython script to retrieve fasta seq from a list of file & count aa
# HB 2020/03/11

import requests as r
from Bio import SeqIO
from io import StringIO
import os
import sys

baseUrl="http://www.uniprot.org/uniprot/"

# Loop
with open(sys.argv[1]) as f:
        # loop through each line
        for line in f:
         # Remove white space
         line = line.strip()
         # If not empty
         if line:
          currentUrl=baseUrl+line+".fasta"
          response= r.post(currentUrl)
          cData=''.join(response.text)
          Seq=StringIO(cData)
          record = list(SeqIO.parse(Seq,"fasta"))
          # Print ID & Sequence Length
          print("%s, %i" % (line, len(record[0].seq)))
          # Sequence output
          #SeqIO.write(record, line + ".fasta", "fasta")



