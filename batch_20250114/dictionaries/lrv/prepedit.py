# coding=utf-8
""" separate.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def split_sections(lines,start):
 sections = []
 current_section = []
 for line in lines:
  if line.startswith(start):
   # If we already have a section collected, save it
   if current_section != []:
    sections.append(current_section)
    current_section = []
  current_section.append(line)
 
 # Add the last section if any
 if current_section:
  sections.append(current_section)

 return sections

def write_sections(fileout,sections):
 outarr = []
 for section in sections:
  for x in section:
   outarr.append(x)
 with codecs.open(fileout,"w","utf-8") as f:
  for out in outarr:
   f.write(out+'\n')
 print(len(sections),"sections written to",fileout)
 
def separate_sections(sections,parmstr):
 a = []  # first line of section begins with parmstr
 b = []  #  the rest
 for section in sections:
  line1 = section[0]
  if line1.startswith(parmstr):
    a.append(section)
  else:
    b.append(section)
 return(a,b)

def sort_sections(sections):
 a = []
 for section in sections:
  case = section[0]
  m = re.search(r'^Case ([0-9]+)',case)
  casenum = int(m.group(1))
  newcase = '* TODO ' + case
  section[0] = newcase
  aval = (casenum,section)
  a.append(aval)
 b = sorted(a)
 newsections = [bval[1] for bval in b]
 return newsections
if __name__ == "__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 lines = read_lines(filein)
 print(f'{len(lines)} lines read from {filein}')
 start = 'Case '
 sections = split_sections(lines,start)
 #write_sections('temp.txt',sections)
 #exit(1)
 header = sections[0] # before first section
 sections1 = sections[1:] # rest of sections
 sections2 = sort_sections(sections1)
 sections2.insert(0,header) 
 write_sections(fileout,sections2)
 
