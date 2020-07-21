#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 00:33:50 2020

Calculate the helical content from PSIPRED prediction
It will write to a csv file

@author: kbui2
"""

import argparse


''' Calculate helical content from a ss2file '''
def calc_helical_content(ss2file):
	ss2 = open(ss2file, 'r')	
	count = 0
	hel = 0
	for line in ss2:
		record = line.split()
		if len(record)==6: # AA line, not header
			count += 1
			if record[2] == 'H':
				hel += 1
				
	return hel/count
			


if __name__=='__main__':	
	parser = argparse.ArgumentParser(description='Automatically submit a list of Uniprot protein to PSIPRED');
	parser.add_argument('--list', help='Input of Uniprot ID list',required=True)
	parser.add_argument('--idir', help='Input directory of the PSIPRED results',required=True)
	parser.add_argument('--o', help='Output csv file',required=True)

	args = parser.parse_args()
	
	listid = open(args.list, 'r')
	pIDlist = listid.read().splitlines()
	listid.close()
	
	outfile = open(args.o, 'w')
	idir = args.idir
	
	for pID in pIDlist:
		ss2file = idir + '/' + pID + '.ss2'
		hcont = calc_helical_content(ss2file)
		outfile.write(pID + ',' + '{:3.1f}'.format(hcont*100) + '\n')
	
	outfile.close()
		
