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
	counter = 0
	result = []
	for line in codecs.open(tsvfile, 'r', 'utf-8'):
		entry = line.rstrip().split('\t')
		if counter <= lst:
			pass
		elif not ':' in entry[-1]:
			date = entry[0]
			dictionary = entry[1].lower()
			lnum = entry[2].lstrip().rstrip()
			headword = entry[3]
			old = entry[4]
			new = entry[5]
			comment = entry[6]
			result.append({'body': 'date:\t' + date + '\n' + 'dict:\t' + dictionary + '\n' + 'Lnum:\t'+ lnum + '\n' + 'hw:\t'+ headword + '\n' + 'old:\t' + old + '\n' + 'new:\t' + new + '\n' + 'comm:\t' + comment, 'title': dictionary + ':' + lnum})
		counter += 1
	codecs.open(lastcfrline, 'w', 'utf-8').write(str(counter))
	return result


def create_issue(entry):
	username = os.environ['GITHUB_USER']
	password = os.environ['GITHUB_PASSWORD']
	print(entry)
	s = requests.Session()
	s.auth = (username, password)
	r = s.post('https://api.github.com/repos/sanskrit-lexicon/csl-orig/issues', json.dumps(entry))
	print(r.text)
	
if __name__ == "__main__":
	tsvfile = sys.argv[1]
	result = read_pending_entries(tsvfile, 'last_cfr_line.txt')
	for entry in result:
		create_issue(entry)

