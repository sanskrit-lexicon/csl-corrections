# coding=utf-8
""" search_inserta.py
"""
from __future__ import print_function
import sys, re,codecs
import digentry  

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines

def write_lines(fileout,lines):
 with codecs.open(fileout,"w","utf-8") as f:
  for line in lines:
   f.write(line + '\n')
 print(len(lines),"lines written to",fileout)
 
def write_outrecs(fileout,outrecs):
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')  
 print(len(outrecs),"cases written to",fileout)

def write_changes(fileout,changes):
 outrecs = []
 for ic,c in enumerate(changes):
  outarr = []
  outarr.append('; -----------------------------------------------------')
  m = re.search(r'<k1>(.*?)<',c.metaline)
  k1 = m.group(1)
  href = 'http://localhost/cologne/simple/mw/%s' % k1
  outarr.append('; %s' % href)
  outarr.append('; case %03d: %s' %(ic+1,c.metaline))
  outarr.append(';    child: %s' % c.comment)
  outarr.append('%s old %s' % (c.lnum,c.oldline))
  outarr.append(';')
  outarr.append('%s new %s' % (c.lnum,c.newline))
  outrecs.append(outarr)
 write_outrecs(fileout,outrecs)

def write_outrecs(fileout,outrecs):
 with codecs.open(fileout,"w","utf-8") as f:
  for outarr in outrecs:
   for out in outarr:
    f.write(out+'\n')  
 print(len(outrecs),"cases written to",fileout)

def write_outarr(fileout,outarr):
 with codecs.open(fileout,"w","utf-8") as f:
   for out in outarr:
    f.write(out+'\n')  
 print(len(outarr),"cases written to",fileout)

class Change:
 def __init__(self,oldline,newline,metaline,comment,lnum):
  # a -> b
  self.oldline = oldline
  self.newline = newline
  self.lnum = lnum
  self.metaline = metaline
  self.comment = comment

def make_changes_helper(eref,e):
 # modify last line of e.datalines
 metaline = e.metaline
 oldline = e.datalines[-1]
 # newline = oldline + '<listinfo n="sup"/>'
 newline = oldline
 comment = eref.metaline
 iline = len(e.datalines) - 1
 lnum = e.linenum1 + iline + 1
 change = Change(oldline,newline,metaline,comment,lnum)
 return change

def make_changes(entries,option):
 changes = []
 changes_made_L = {}
 m = re.search(r'^([1-4])([A-Z]*)$',option)
 assert m != None
 optionnum = m.group(1)
 optionsfx = m.group(2)
 
 for ientry,e in enumerate(entries):
   metaline = e.metaline
   body = ' ' . join(e.datalines)
   supflag = ('<info n="sup"/>' in body)
   if not supflag:
    continue
   # this entry is a sup.
   Hcode = e.metad['e']
   if Hcode != option:
    continue
   # so Hcode == option
   m = re.search(r'^([1-4])([A-Z]*)$',Hcode)
   assert m != None
   Hcodenum = m.group(1)
   Hcodesfx = m.group(2)
  #  <e>NA
   ieprev = ientry
   eprev = entries[ieprev]
   while True:
    ieprev = ieprev - 1
    eprev = entries[ieprev]
    Hcodeprev = eprev.metad['e']
    if not Hcodeprev in ['1','2','3','4']:
     continue
    break 
   # ?if (Hcodeprev + 'A') != Hcode:
   # continue
   bodyprev = ' ' . join(eprev.datalines)
   if '<listinfo n="sup"/>' in bodyprev: 
    # eprev already modified
    continue
   Lprev = eprev.metad['L']
   if Lprev in changes_made_L:
    # previously changed
    continue
   changes_made_L[Lprev] = True
   # this is a candidate:
   change = make_changes_helper(e,eprev)
   changes.append(change)
 #nchanges = len(changes)
 #print('%s changes identified' % nchanges)
 #print('exit debug')
 #exit(1)
 return changes

def  mark_mwlines(mwlines,changes):
 d = {}
 for ic,c in enumerate(changes):
  m = re.search(r'^<L>(.*?)<',c.metaline)
  L = m.group(1)
  # L may be duplicate
  if L not in d:
   d[L] = []
  d[L].append(ic+1)
 #
 newlines = []
 for iline,line in enumerate(mwlines):
  m = re.search(r'^<L>(.*?)<pc>(.*?)<k1>(.*?)<k2>',line)
  if m == None:
   newlines.append(line)
   continue
  # metaline
  L = m.group(1)
  pc = m.group(2)
  k1 = m.group(3)
  if L not in d:
   # no correction for this entry
   newlines.append(line)
   continue
  cases = d[L]  # list of correction cases
  cases1 = [str(case) for case in cases]
  cases_str = ','.join(cases1)
  pfx = '* case %s ' % cases_str
  # add a link to printed page
  #href = 'http://localhost/cologne/csl-apidev/servepdf.php?dict=mw&page=%s' % pc
  dictlo = 'mw'  
  href = 'http://localhost/cologne/simple/%s/%s' % (dictlo,k1)
  newline = pfx + line + '  ' + href
  newlines.append(newline)  
  # mark associated <LEND>
  iline1 = iline
  while True:
   iline1 = iline1 + 1
   line1 = mwlines[iline1]
   if line1.startswith('<LEND>'):
    line1a = '* ' + line1
    mwlines[iline1] = line1a
    break
 return newlines

if __name__=="__main__":
 option = sys.argv[1]
 filein = sys.argv[2]  # xxx.txt
 fileout = sys.argv[3] # change transactions
 fileout1 = sys.argv[4] # marked version of filein
 entries = digentry.init(filein)
 changes = make_changes(entries,option)
 print(len(changes),"lines changes")
 write_changes(fileout,changes)
 mwlines = read_lines(filein)
 
 mwnewlines = mark_mwlines(mwlines,changes)
 write_lines(fileout1,mwnewlines)
