""" python upload_github_issue.py app/correction_response/cfr1.tsv
	Dr. Dhaval Patel
	19 October 2019
"""
from __future__ import print_function
import re
import sys
import os
import codecs

def read_pending_entries(tsvfile):
	counter = 1
	result = []
	for line in codecs.open(tsvfile, 'r', 'utf-8'):
		entry = line.rstrip().split('\t')
		if counter == 1:
			pass
		elif not ':' in entry[-1]:
			if len(entry) == 8:
				print(counter)
				date = entry[0]
				dictionary = entry[1].lower()
				lnum = entry[2].lstrip().rstrip()
				headword = entry[3]
				old = entry[4]
				new = entry[5]
				comment = entry[6]
				email = entry[7]
				result.append({'body': 'date:\t' + date + '\n' + 'dict:\t' + dictionary + '\n' + 'Lnum:\t'+ lnum + '\n' + 'hw:\t'+ headword + '\n' + 'old:\t' + old + '\n' + 'new:\t' + new + '\n' + 'comm:\t' + comment + '\n' + 'email:\t'+ email, 'title': dictionary + ':' + lnum})
		counter += 1
	return result
	
if __name__ == "__main__":
	tsvfile = sys.argv[1]
	result = read_pending_entries(tsvfile)
	for entry in result:
		print(entry)

