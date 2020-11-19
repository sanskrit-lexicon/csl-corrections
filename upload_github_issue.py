""" python upload_github_issue.py app/correction_response/cfr.tsv
	Dr. Dhaval Patel
	19 October 2019
"""
from __future__ import print_function
import re
import sys
import os
import codecs
import requests
import json

def read_pending_entries(tsvfile, lastcfrline):
	lst = int(codecs.open(lastcfrline, 'r', 'utf-8').read())
	#print('lst=',lst)
	counter = 0
	result = []
	pending_lines = [] # the lines and counter values corresponding to result
	for line in codecs.open(tsvfile, 'r', 'utf-8'):
		entry = line.rstrip().split('\t')
		if counter < lst:
			pass
		elif not ':' in entry[-1]:
			date = entry[0]
			dictionary = entry[1].lower()
			lnum = entry[2].lstrip().rstrip()
			headword = entry[3]
			old = entry[4]
			new = entry[5]
			comment = entry[6]
			bodytxt = 'date:\t' + date + '\n' + 'dict:\t' + dictionary + '\n' + 'Lnum:\t'+ lnum + '\n' + 'hw:\t'+ headword + '\n' + 'old:\t' + old + '\n' + 'new:\t' + new + '\n' + 'comm:\t' + comment
			title=dictionary + ':' + lnum
			result.append({'body': bodytxt,'title':title})
			pending_line = (counter,line)
			pending_lines.append(pending_line)
			print(pending_line) # dbg
		counter += 1
	#print('ending counter=',counter)
	#codecs.open(lastcfrline, 'w', 'utf-8').write(str(counter))  #Do this in create_issue
	return pending_lines,result


def create_issue(entry):
	username = os.environ['GITHUB_USER']
	#password = os.environ['GITHUB_PASSWORD']
	token = os.environ['GITHUB_ACCESS_TOKEN']
	#print(username,password)
	#print('entry=',entry)
	s = requests.Session()
	#s.auth = (username, password)
	s.auth = (username, token)
	r = s.post('https://api.github.com/repos/sanskrit-lexicon/csl-orig/issues', json.dumps(entry))
	#print('status code returns:',r.status_code)
	#if r.status_code == requests.codes.created:
	#	print(r.text)
	return r.status_code
	
if __name__ == "__main__":
	tsvfile = sys.argv[1]
	lastcfrline = 'last_cfr_line.txt'
	pending_lines,result = read_pending_entries(tsvfile, lastcfrline)
	#print('result length=',len(result))
	if len(result) == 0:
		print('no new entries to post')
	for ientry,entry in enumerate(result):
		counter,line = pending_lines[ientry]
		status = create_issue(entry)
		# requests.codes.ok  is actually '200'.
		# But when a resource is being created, requests returns '201'
		# We are creating a resource, so we want to check for 201
		# requests.codes.created is 201
		if status == requests.codes.created:
			#update last_cfr_file
			# note the '+1'
			print('uploaded issue',entry['title'])
			codecs.open(lastcfrline, 'w', 'utf-8').write(str(counter+1))
		else:
			# some problem
			print('Error posting: requests status = ',status)
			print('counter = ',counter)
			print('line = ',line)
			break
