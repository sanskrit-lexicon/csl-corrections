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

def get_ymd(line):
 parts = line.split('\t')
 datetime = parts[0]
 date,time = datetime.split(' ')
 m,d,y = date.split('/')
 im = int(m)
 id = int(d)
 iy = int(y)
 ymd = '%04d%02d%02d' %(iy,im,id)
 return ymd # a string yyyymmdd

def partiion_lines(lastymd,lines):
 lines1 = []  # <= lastymd, also title
 lines2 = []
 lines3 = []
 lines4 = []
 pat2 = '\tsrhodes@snowcrest.net'
 scott_dicts = {}
 for iline,line in enumerate(lines):
  lnum = iline + 1
  if iline == 0:
   lines1.append(line)  # title
   continue
  curymd = get_ymd(line)
  if (curymd <= lastymd):
   # processed lines
   lines1.append(line)
  elif (pat2 in line):
   # unprocessed Scott-mw lines
   lines2.append(line)
   update_scott_dicts(scott_dicts,line)
  elif empty_dict(line):
   lines4.append(line)
  else: # other unprocessed lines   
   lines3.append(line)
 
 return lines1,lines2,lines3,lines4,scott_dicts

if __name__=="__main__":
 #lastlnum = int(sys.argv[1])  # /last_cfr_line.txt
 lastymd = sys.argv[1]  # yyyymmdd
 filein = sys.argv[2]  # cfr.tsv
 fileout1 = sys.argv[3] # prev.tsv  <= lastymd
 fileout2 = sys.argv[4] # scott.tsv :  > lastymd AND scott
 fileout3 = sys.argv[5] # notscott.tsv : > lastymd AND not scott
 fileout4 = sys.argv[6] # deleted.tsv
 lines = read_lines(filein)
 lines1,lines2,lines3,lines4,scott_dicts = partiion_lines(lastymd,lines)
 write_lines(fileout1,lines1)
 write_lines(fileout2,lines2)  # scott
 for dictname in scott_dicts:
  n = scott_dicts[dictname]
  print('  Scott: %s %s' % (dictname,n))
 write_lines(fileout3,lines3)
 write_lines(fileout4,lines4)


