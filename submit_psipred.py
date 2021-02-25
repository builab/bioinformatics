#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 00:33:50 2020
Last modified 20210226 fix urllib.request, need to type python3 submit_psipred
For psipred, fasta file must be clean without the header
Skip protein > 1500A (limit of psipred)
Ignore_exsisting function


Script to submit a list of Uniprot ID for PSIPRED prediction
It will automatically download the Uniprot fasta file and submit
then download the results to the same directory

See further
http://bioinf.cs.ucl.ac.uk/web_servers/web_services/

@author: kbui2
"""

import requests
import urllib, argparse, os, time, urllib.request
import os.path


""" Submit psipred job """

def psipredSubmit(pID, filepath, email):
	url = 'http://bioinf.cs.ucl.ac.uk/psipred/api/submission.json'
	filename = os.path.basename(filepath)
	payload = {'input_data': (filename, open(filepath, 'rb'))}
	data = {'job': 'psipred',
        	'submission_name': pID,
       		'email': email, }
	r = requests.post(url, data=data, files=payload)
	dict = r.json()
	uuid = dict['UUID']
	return uuid

""" Get psipred job status """

def psipredProgress(uuid):
	# Not done yet
	url = 'http://bioinf.cs.ucl.ac.uk/psipred_new/api/submission/'
	params = {'format': 'json'}
	r = requests.get(url + uuid, params=params)
	dict = r.json()
	return dict
	
""" Get psipred job results ss2, horiz file """

def psipredDownload(ss2, pID, outdir):
	""" Download ss2 file """
	url = 'http://bioinf.cs.ucl.ac.uk/psipred/api'	
	# SS2 file
	r = requests.get(url + ss2)	
	with open(outdir + '/' + pID + '.ss2','wb') as f:
		f.write(r.content)	
	f.close()
    	# Horiz file
	r2 = requests.get(url + str.replace(ss2, '.ss2', '.horiz'))	
	with open(outdir + '/' + pID + '.horiz','wb') as f2:
		f2.write(r2.content)
	f2.close()
		
		      
""" Retrieve the fasta sequence from uniprot ID and write to an output file """

def retrieveFasta(pID, outfile):
	print('Retrieving ' + pID)
	response = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + pID + ".fasta").read()
	content = response.decode('utf-8')
	outhandle = open(outfile, 'w')
	outhandle.write(content)
	outhandle.close()
	
def trimFasta(file, trimfile):
	""" Trim the header with > of fasta file """
	fastain = open(file, 'r')
	fastaout = open(trimfile, 'w')
	for line in fastain:
		if line[0] == '>':
			continue
		fastaout.write(line)
	fastain.close()
	fastaout.close()
	
def calcFastaLength(file):
	""" Calc the length of fasta file """
	fastain = open(file, 'r')
	aalen = 0
	for line in fastain:
		if line[0] == '>':
			continue
		aalen = aalen + len(line)
	
	fastain.close()
	return aalen

if __name__=='__main__':	
	parser = argparse.ArgumentParser(description='Automatically submit a list of Uniprot protein to PSIPRED');
	parser.add_argument('--list', help='Input of Uniprot ID list',required=True)
	parser.add_argument('--email', help='Email for job submission',required=False,default='huy.bui@mcgill.ca')
	parser.add_argument('--odir', help='Output directory for output',required=True)
	parser.add_argument('--ignore_existing', help='Ignore existing file (1/0)',required=False,default='0')

	args = parser.parse_args()
	
	# Limit of PSIPRED
	PSIPREDLIMIT = 1500
	
	listid = open(args.list, 'r')
	pIDlist = listid.read().splitlines()
	listid.close()
	
	email = args.email
	outdir = args.odir
	
	ignore_existing = int(args.ignore_existing)
	
	for pID in pIDlist:
		outfile = outdir + '/' + pID + '_full.fasta'
		trimfile = outdir + '/' + pID + '.fasta'

		retrieveFasta(pID, outfile)
		trimFasta(outfile, trimfile)
		
		
		if calcFastaLength(trimfile) > PSIPREDLIMIT:
			print('Skip due to length limit')
			continue
			
		print ('AA length ' + str(calcFastaLength(trimfile)))
		if os.path.exists(outdir + "/" + pID + ".ss2") and ignore_existing == 1:
			print('Skip ' + pID + ' due to existing file')
			continue
		
		print('Submit ' + trimfile)

		uuid = psipredSubmit(pID, trimfile, email)
		while True:
			time.sleep(300)
			dict = psipredProgress(uuid)
			print('Job ' + uuid + ' is ' + dict['state'])
			if dict['state'] == 'Complete':
				break
	
		out = dict['submissions'][0]['results']
		# It seems to change now, becareful with this by debugging
		# print(out)
		ss2 = out[1]['data_path']
		
	
	
		print ('Download results')
		psipredDownload(ss2, pID, outdir)
