# coding=utf-8
""" search_insert.py
"""
from __future__ import print_function
import sys, re,codecs
import digentry  

def read_lines(filein):
 with codecs.open(filein,encoding='utf-8',mode='r') as f:
  lines = [x.rstrip('\r\n') for x in f]
 return lines


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
 newline = oldline + '<listinfo n="sup"/>'
 comment = eref.metaline
 iline = len(e.datalines) - 1
 lnum = e.linenum1 + iline + 1
 change = Change(oldline,newline,metaline,comment,lnum)
 return change

def make_changes_1(entries):
 changes = []
 for ientry,e in enumerate(entries):
   metaline = e.metaline
   body = ' ' . join(e.datalines)
   supflag = ('<info n="sup"/>' in body)
   if not supflag:
    continue
   # this entry is a sup.
   Hcode = e.metad['e']
   if not Hcode.endswith('A'):
    continue
   #  <e>2A
   ieprev = ientry - 1
   eprev = entries[ieprev]
   Hcodeprev = eprev.metad['e']
   if not Hcodeprev in ['1','2','3','4']:
    continue
   if (Hcodeprev + 'A') != Hcode:
    continue
   bodyprev = ' ' . join(eprev.datalines)
   if '<listinfo n="sup"/>' in bodyprev: 
    # eprev already modified
    continue
   # this is a candidate:
   change = make_changes_helper(e,eprev)
   changes.append(change)
 nchanges = len(changes)
 #print('%s changes identified' % nchanges)
 #print('exit debug')
 #exit(1)
 return changes

def make_changes_2(entries):
 changes = []
 changes_made_L = {}
 for ientry,e in enumerate(entries):
   metaline = e.metaline
   body = ' ' . join(e.datalines)
   supflag = ('<info n="sup"/>' in body)
   if not supflag:
    continue
   # this entry is a sup.
   Hcode = e.metad['e']
   m = re.search(r'^([1-4])([A-Z]*)$',Hcode)
   assert m != None
   Hcodenum = m.group(1)
   Hcodesfx = m.group(2)
   if not (Hcodesfx == 'A'):
    continue
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
   if (Hcodeprev + 'A') != Hcode:
    continue
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

def count_sup(entries):
 d = {}
 for ientry,e in enumerate(entries):
  metaline = e.metaline
  body = ' ' . join(e.datalines)
  supflag = ('<info n="sup"/>' in body)
  if not supflag:
   continue
  Hcode = e.metad['e']
  if Hcode not in d:
   d[Hcode] = 0
  d[Hcode] = d[Hcode] + 1
 for Hcode in d:
  count = d[Hcode]
  print('%2s %s' % (Hcode,count))

if __name__=="__main__":
 option = sys.argv[1]
 filein = sys.argv[2]  # xxx.txt
 fileout = sys.argv[3] # change transactions
 entries = digentry.init(filein)
 if option == '1':
  changes = make_changes_1(entries)
 elif option == '2':
  changes = make_changes_2(entries)
 elif option == 'count':
  count_sup(entries)
  exit(1) # no file output
 else:
  print('ERROR: unknown option',option)
  exit(1)
 print(len(changes),"lines changes")
 write_changes(fileout,changes)

