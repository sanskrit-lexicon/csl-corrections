""" remove_markup.py
"""
from __future__ import print_function
import re,sys,os
import codecs

def read_lines(filein):
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip() for x in f]
 print(len(lines),"lines read from",filein)
 return lines

def write_lines(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line + '\n')
 print(len(lines),"lines written to",fileout)

def  mark_mwlines_remove(mwlines):
 newlines = []
 for iline,line in enumerate(mwlines):
  if not line.startswith('*'):
   newlines.append(line)
   continue
  if line.startswith('* <LEND>'):
   newline = '<LEND>'
   newlines.append(newline)
   continue
  # metaline
  newline = re.sub(r'^[*].*<L>', '<L>',line)
  newline = re.sub(r' *http://.*$','',newline)
  newlines.append(newline)
 return newlines

if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 mwlines = read_lines(filein)
 mwnewlines = mark_mwlines_remove(mwlines)
 write_lines(fileout,mwnewlines)

