#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Script to convert database ID using Uniprot API
# Last updated: 2020/07/11 
# Author: ChelseaDB, HuyBui

import urllib.parse 
import urllib.request
import argparse
from argparse import RawTextHelpFormatter

url = 'https://www.uniprot.org/uploadlists/'
	
""" 
	This function is used to convert an ID from 1 database (fromDb) into another ID 
	from another database (toDb). It will write to a csv file of an open file.
	
"""
	
def Convert(fromDb, toDb, queryString, outfile):
	params = {
	'from' : fromDb, #ACC+ID = UniProtKB AC/ID
	'to' : toDb, #RefSeq Protein = NCBI protein 
						  # or P_ENTREZGENEID  NCBI gene
	'format': 'tab',
	'query' : queryString 
	}
	
	data = urllib.parse.urlencode(params)
	data = data.encode('utf-8')
	req = urllib.request.Request(url, data)
	with urllib.request.urlopen(req) as f:
		response = f.read()
		content = response.decode('utf-8')
		
	content = content.splitlines()
	for line in content:
		records = line.split()
		if (records[0] != 'From'):
			writecsvline(outfile, records)
			
			
def writecsvline(outfile,records):
	"""Write a record (line) to an already open csv file"""
	for item in records[:-1]:
		outfile.write(item+',')
	outfile.write(records[-1])
	outfile.write('\n')
	
		
if __name__=='__main__':
	parser = argparse.ArgumentParser(description="""Convert list of databaseID (Default: uniprot ID to NCBI)  
    See more DatabaseID at https://www.uniprot.org/help/api_idmapping
		Uniprot\t\tACC+ID
		NCBI protein\tP_REFSEQ_AC
		NCBI gene\tP_ENTREZGENEID
    Example: 
		python ./convertingUniprot-NCBI_list.py --i list_uniprot.txt --o out.csv --fromdb ACC+ID --todb P_ENTREZGENEID""", 
								  usage='%(prog)s [OPTIONS]',
								  formatter_class=RawTextHelpFormatter)
	parser.add_argument('--i', help='Input of ID list',required=True)
	parser.add_argument('--o', help='Output csv file',required=True)
	parser.add_argument('--fromdb', help='Input database (default=Uniprot/ACC+ID)',required=False,default='ACC+ID')
	parser.add_argument('--todb', help='Output database (default=NCBI/P_REFSEQ_AC)',required=False,default='P_REFSEQ_AC')

	args = parser.parse_args()
	fromDb = args.fromdb
	toDb = args.todb
	
	outfile = open(args.o, 'w')
	
	with open(args.i) as f:
		query = ' '.join(line.rstrip() for line in f)
		
		#print(query)
	print ('Converting from ' + fromDb + ' to ' + toDb)
	outfile.write(fromDb + ',' + toDb + '\n')
	Convert(fromDb, toDb, query, outfile)
	
	outfile.close()