#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 00:33:50 2020
Last modified 20210701


Script to submit a list of Uniprot ID for PSIPRED prediction
It will automatically download the Uniprot fasta file and submit
then download the results to the same directory

See further
http://bioinf.cs.ucl.ac.uk/web_servers/web_services/

@author: kbui2
"""


import requests
import urllib, argparse, os, time


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

def psipredDownload(datapath, pID, outdir):
	url = 'http://bioinf.cs.ucl.ac.uk/psipred/api'
	
	# SS2 file
	r = requests.get(url + ss2)
	
	with open(outdir + '/' + pID + '.ss2','wb') as f:
		   f.write(r.content)
		   
    # Horiz file
	r2 = requests.get(url + str.replace(ss2, '.ss2', '.horiz'))
	
	with open(outdir + '/' + pID + '.horiz','wb') as f:
		   f.write(r2.content)
		      
""" Retrieve the fasta sequence from uniprot ID and write to an output file """

def retrieveFasta(pID, outfile):
	print('Retrieving ' + pID)
	response = urllib.request.urlopen("http://www.uniprot.org/uniprot/" + pID + ".fasta").read()
	content = response.decode('utf-8')
	outhandle = open(outfile, 'w')
	outhandle.write(content)
	outhandle.close()


if __name__=='__main__':	
	parser = argparse.ArgumentParser(description='Automatically submit a list of Uniprot protein to PSIPRED');
	parser.add_argument('--list', help='Input of Uniprot ID list',required=True)
	parser.add_argument('--email', help='Email for job submission',required=False,default='huy.bui@mcgill.ca')
	parser.add_argument('--odir', help='Output directory for output',required=True)

	args = parser.parse_args()
	
	listid = open(args.list, 'r')
	pIDlist = listid.read().splitlines()
	listid.close()
	
	email = args.email
	outdir = args.odir
	
	for pID in pIDlist:
		outfile = outdir + '/' + pID + '.fasta'
		retrieveFasta(pID, outfile)
		
		print('Submit ' + outfile )

		uuid = psipredSubmit(pID, outfile, email)
		while True:
			time.sleep(300)
			dict = psipredProgress(uuid)
			print('Job ' + uuid + ' is ' + dict['state'])
			if dict['state'] == 'Complete':
				break
	
		out = dict['submissions'][0]['results']
		ss2 = out[5]['data_path']
	
		print ('Download results')
		psipredDownload(ss2, pID, outdir)
