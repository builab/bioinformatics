#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 00:33:50 2020

Script to retrieve separate FASTA file from a list of uniprot ID

@author: kbui2
"""

import urllib, argparse, time

""" Retrieve the fasta sequence from uniprot ID and write to an output file """

def retrieveFasta(pID, outfile):
	print('Retrieving ' + pID)
	response = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + pID + ".fasta").read()
	content = response.decode('utf-8')
	outhandle = open(outfile, 'w')
	outhandle.write(content)
	outhandle.close()
	
if __name__=='__main__':
	parser = argparse.ArgumentParser(description='Retrieve sequence of Uniprot ID')
	parser.add_argument('--i', help='Input of ID list',required=True)
	parser.add_argument('--odir', help='Output directory location',required=True)

	args = parser.parse_args()
	
	outdir = args.odir
	
	list = open(args.i, 'r')
	
	
	for line in list:
		line = line.strip()
		if line:
			out = outdir + '/' + line + '.fasta'
			retrieveFasta(line, out)
		time.sleep(5)
		
	list.close()