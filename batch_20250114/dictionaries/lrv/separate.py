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

if __name__ == "__main__":
 parmstr = sys.argv[1]
 filein = sys.argv[2]
 fileout1 = sys.argv[3]
 fileout2 = sys.argv[4]
 lines = read_lines(filein)
 print(f'{len(lines)} lines read from {filein}')
 start = '* '
 sections = split_sections(lines,start)
 #write_sections('temp.txt',sections)
 #exit(1)
 if not sections[0][0].startswith(start):
  # skip this first section
  print('skipping first section, whose first line is')
  print(sections[0][0])
  sections = sections[1:]
 print(f'{len(sections)} sections')
 sections1,sections2 = separate_sections(sections,parmstr)
 write_sections(fileout1,sections1)
 write_sections(fileout2,sections2)
 
