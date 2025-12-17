# coding=utf-8
""" markhom.py
"""
from __future__ import print_function
import sys, re,codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

class Change(object):
 def __init__(self,iline,line1,line2,metaline1):
  self.iline = iline
  self.line1 = line1
  self.line2 = line2
  self.lnum = iline+1
  self.metaline1 = metaline1 
  a = []
  a.append('; %s' %metaline1)
  a.append('%s old %s' %(self.lnum,self.line1))
  a.append(';')
  a.append('%s new %s' %(self.lnum,self.line2))
  a.append(';---------------------------------------------------')
  self.changeout = a
  
def write_lines(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in lines:
   f.write(out+'\n')

hom_map = {'I':1, 'II':2, 'III':3, 'IV':4, 'V':5}
def mark_helper(metaline,nextline):
 m = re.search(r'<h>',metaline)
 if m != None:
  print('already marked',metaline)
  return metaline
 # example of nextline with homonym:
 # {#aMSula#}¦ {%(II) m.%} 
 m = re.search(r'¦ {%\((.*?)\)',nextline)
 if m == None:
  # not a homonym
  return metaline
 rawhom = m.group(1)
 if rawhom not in hom_map:
  print(f'unexpected rawhom = {rawhom}')
  print(f'  metaline = {metaline}')
  return metaline
 # alter metaline
 hom = hom_map[rawhom]
 newmeta = f'{metaline}<h>{hom}'
 return newmeta

def mark(lines):
 newlines = []
 nchg = 0
 for iline,line in enumerate(lines):
  if not line.startswith('<L>'):
   newlines.append(line)
   continue
  # line is a metaline
  nextline = lines[iline+1]
  newline = mark_helper(line,nextline)
  if newline != line:
   nchg = nchg + 1
  newlines.append(newline)
 print(f'{nchg} lines changed')
 return newlines
if __name__=="__main__":
 filein = sys.argv[1] # old.txt
 fileout =sys.argv[2] # new.txt
 lines = read_lines(filein)
 newlines = mark(lines)
 write_lines(fileout,newlines)

