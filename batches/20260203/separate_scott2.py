"""
separate_scott.py 
01-14-2025
"""
#
from __future__ import print_function
import re,sys
import codecs

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 print(len(lines),"lines read from",filein)
 return lines

def write_lines(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for out in lines:
   f.write(out+'\n')
 print(len(lines),"lines written to",fileout)

def update_scott_dicts(d,line):
 parts = line.split('\t')  # the different fields of line from cfr.tsv
 dictname = parts[1]  # 2nd field
 if dictname not in d:
  d[dictname] = 0
 d[dictname] = d[dictname] + 1

def empty_dict(line):
 parts = line.split('\t')  # the different fields of line from cfr.tsv
 dictname = parts[1]  # 2nd field
 a = dictname.strip()  # remove whitespace (blank or \t)
 return a == ''  #empty dict

def partiion_lines(dt,lines):
 lines1 = []
 lines2 = []
 lines3 = []
 lines4 = []
 pat2 = '\tsrhodes@snowcrest.net'
 scott_dicts = {}
 dtregex = r'^([0-9]+)/([0-9]+)/([0-9]+) ([0-9]+):([0-9]+):([0-9]+)$'
 for iline,line in enumerate(lines):
  lnum = iline + 1
  parts = line.split('\t')
  dtline0 = parts[0].strip()
  if iline == 0:
   # first line is a title line.
   # put it into prev.tsv
   lines1.append(line)
   continue
  m = re.search(dtregex,dtline0)
  if m == None:
   print('partition_lines problem with date-time field at line',lnum)
   print(dtline0)
   exit(1)
  mm = int(m.group(1))
  dd = int(m.group(2))
  yyyy = int(m.group(3))
  hh = int(m.group(4))
  nn = int(m.group(5))
  ss = int(m.group(6))
  dtline = f'{yyyy:04d}{mm:02d}{dd:02d} {hh:02d}:{nn:02d}:{ss:02d}'
  #print(f'dtline0={dtline0}\ndtline={dtline}')
  #exit(1)
  if dtline <= dt:
   # prev.tsv
   lines1.append(line)
  elif (pat2 in line):
   # unprocessed Scott-mw lines
   lines2.append(line)  # scott.tsv
   update_scott_dicts(scott_dicts,line)
  elif empty_dict(line):
   lines4.append(line)  # deleted.tsv
  else: # other unprocessed lines notscott.tsv
   lines3.append(line)
 
 return lines1,lines2,lines3,lines4,scott_dicts

if __name__=="__main__":
 dt = sys.argv[1]  # date-time string e.g. '20250417 12:34:45'
 filein = sys.argv[2]  # current cfr.tsv
 fileout1 = sys.argv[3] # previous cfr.tsv  lines 1- lastlnum
 fileout2 = sys.argv[4] # scott.tsv
 fileout3 = sys.argv[5] # notscott.tsv
 fileout4 = sys.argv[6] # deleted.tsv probable mal-formed lines
 lines = read_lines(filein)
 lines1,lines2,lines3,lines4,scott_dicts = partiion_lines(dt,lines)
 write_lines(fileout1,lines1)
 write_lines(fileout2,lines2)  # scott
 for dictname in scott_dicts:
  n = scott_dicts[dictname]
  print('  Scott: %s %s' % (dictname,n))
 write_lines(fileout3,lines3)
 write_lines(fileout4,lines4)


