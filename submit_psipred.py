#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 12 00:33:50 2020

Script to retrieve separate FASTA file from a list of uniprot ID

See further
http://bioinf.cs.ucl.ac.uk/web_servers/web_services/

@author: kbui2
"""


import os, time
import requests


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
		   
   
   #NOTE: Once posted you will need to use the GET submission endpoint
#to retrieve your results. Polling the server about once every 2 or 5 mins
#should be sufficient.
#
# Full details at http://bioinf.cs.ucl.ac.uk/web_servers/web_services/


if __name__=='__main__':	
	
	pIDlist = ['P41352', 'I7M9N6', 'Q7Z2D1']

	
	email = 'huy.bui@mcgill.ca'
	path = '/Users/kbui2/Desktop/python/dirp/fasta/'
	outdir = path
	
	for pID in pIDlist:
		filepath = path + pID + '.fasta'
		print('Submit ' + filepath )

		uuid = psipredSubmit(pID, filepath, email)
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