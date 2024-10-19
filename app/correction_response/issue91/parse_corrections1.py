""" parse_corrections1.py 
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
 
def oneline(x):
 parts = re.split(r'[\r\n]',x)
 y = ' '.join(parts)
 return y

class CFR(object):
 def __init__(self,line,n):
  parts = line.split('\t')
  self.line = line
  self.n = n
  if len(parts)!= 8:
   print("# of tab-parts should be 8, but is",len(parts))
   out = "Error 1 for line %s:\n%s" %(n,line)
   print(out.encode('utf-8'))
   exit(1)
  self.time = oneline(parts[0])
  # Jul 18, 2015 - Generate a sortable timefield
  # Assume time is mm/dd/yyyy hh:mm:ss
  # Change to yyyymmdd-hh:mm:ss-nnnn  (nnnnnn = self.n)
  try:
   timeparts = re.split(r'[/: ]',self.time)
   mm = int(timeparts[0])
   dd = int(timeparts[1])
   yyyy = int(timeparts[2])
   h = int(timeparts[3])
   m = int(timeparts[4])
   s = int(timeparts[5])
   self.sorttime = "%4d%02d%02d-%02d%02d%02d-%06d" %(yyyy,mm,dd,h,m,s,n)
  except:
   if n != 1:
    print("ERROR time='%s'" % self.time)
    print(n,line.encode('utf-8'))
    print(re.split(r'[/: ]',self.time))
    exit()
   else: # case n=1
    (mm,dd,yyyy,h,m,s) = (0,0,0,0,0,0)
    self.sorttime = "%4d%02d%02d-%02d%02d%02d-%06d" %(yyyy,mm,dd,h,m,s,n)
  self.dict = oneline(parts[1])
  if self.dict == "APES":
   self.dict = "AE"
  elif self.dict == "PWG2013":
   self.dict = "PWG"
  self.lnum = oneline(parts[2])
  self.hw = oneline(parts[3])
  self.old = oneline(parts[4])
  self.new = oneline(parts[5])
  self.comment = oneline(parts[6])
  email = oneline(parts[7])
  self.email = email.rstrip()
  eparts = email.split(r':')
  if len(eparts) >= 2:
   self.user = eparts[0]
   self.status = ':'.join(eparts[1:])
  else:
   self.user = email
   self.status = ''
  self.user = self.user.strip()
  #if self.user == '':
  # self.user='NONE'
  self.useradj = re.sub(r'@.*$','',self.user)
  # sort on lnum, treated as float
  try:
   L = float(self.lnum)
   self.L = L
  except:
   print('CFR error lnum:',self.lnum)
   print(line)
   self.L = 0.0
   
 def listform(self):
   return [self.time,self.dict,self.lnum,self.hw,self.old,self.new,self.comment,self.useradj,self.status]

def outputrec(rec,i):
 outar=[]
 (date,time) = rec.time.split(' ')
 out = "Case %s: %s dict=%s, L=%s, hw=%s, user=%s" %(
   rec.n,date,rec.dict,rec.lnum,rec.hw,rec.useradj)
 outar.append(out)
 outar.append("old = %s" % rec.old)
 outar.append("new = %s" % rec.new)
 if rec.comment != 'Typo':
  outar.append('comment = %s' % rec.comment)
 if rec.status == '':
  rec.status = 'PENDING'
 outar.append('status = %s' % rec.status)
 outar.append('-'*72)
 outar.append('')
 return outar

def generate_output(dcode,filename,recs):
 allarr =[] # array of all output lines
 #print('generate_output: dcode=',dcode)
 if dcode == "ALL":
  out = "Sanskrit Lexicon Correction Form History"
 else:
  out = "Sanskrit Lexicon Correction Form History for %s" % dcode
 allarr.append(out)
 import datetime
 today = datetime.date.today()
 date = today.strftime("%B %d, %Y")
 out = "As of %s" % date 
 allarr.append(out)
 idxpending = len(allarr) # prepare place-holder
 allarr.append("DUMMY") 
 allarr.append("")
 #fout.write("%s\n" % out)
 #fout.write("\n")
 m = len(recs)
 npending=0
 nfound = 0
 # recs is in ascending order of sorttime.  Read array backwards
 # so new data at the top.
 for i in range(m-1,-1,-1):
  rec = recs[i]
  if not (dcode in ['ALL',rec.dict.upper()]):  
   continue
  nfound = nfound + 1
  outar = outputrec(rec,i)
  for out in outar:
   allarr.append(out)
   if out == 'status = PENDING':
    npending=npending + 1
 # Fill allarr[idxpending]
 allarr[idxpending]="%s correction records, with %s PENDING" %(nfound,npending)
 # generate fileout from dcode and filename
 if dcode == "ALL":
  fileout = filename
 else:
  dir = "%s/%s" %("dictionaries",dcode.lower())
  # example: dcode = MW. filename = correctionform.txt
  # fileout = dictionaries/mw_correctionform.txt
  fileout = "%s/%s_%s" %(dir,dcode.lower(),filename)
  if not os.path.isdir(dir):
   if os.path.exists(dir):
    print("ERROR: %s exists, but is not a directory" % dir)
    exit(1)
   print('ERROR: Missing directory',dir)
   exit(1)
   #os.mkdir(dir,0755)
 if dcode != 'ALL':
  write_flag = check_for_new(allarr,fileout)
 else: # always rewrite the global correctionform.txt file
  write_flag = True
 if write_flag:
  print('rewriting',fileout,'(',npending,'pending )')
  fout = codecs.open(fileout,'w','utf-8')
  for out in allarr:
   fout.write("%s\n" % out)
  fout.close()
  #if dcode != 'ALL':
  # print('debug exit')
  # exit(1)
 elif npending != 0:
  print(fileout,'(',npending,'pending )')
 else:
  #print('No need to rewrite',fileout)
  pass
 return npending

def check_for_new(allarr,fileout):
 """ returns flag indicating whether there is new
     information in allarr
 """
 if not os.path.exists(fileout):
  return True  # we need to rewrite this file
 # fileout exists.  Get its lines
 with codecs.open(fileout,"r","utf-8") as f:
  lines = [x.rstrip() for x in f]
 # compare allarr with lines
 if len(allarr) != len(lines):
  return True  
 # same number of lines.  Probably no new info
 # the 2nd line 'As of MONTH DD, yyyy' This will differ.
 # but we expect other lines to be the same
 rewrite = False
 ndiff = 0
 for i,line in enumerate(lines):
  new = allarr[i]
  if i == 1:
   continue # 2nd line
  if new.rstrip() != line.rstrip():
   ndiff = ndiff + 1
   rewrite = True
   #print('old ',i+1,line.encode('utf-8'))
   #print('new ',i+1,new.encode('utf-8'))
 #print(ndiff,'differences in',fileout)
 return rewrite

def adjust(filein,fileout):
 f = codecs.open(filein,'r','utf-8')
 n = 0
 recsin=[]
 dictmap = {}
 for line in f:
  line = line.rstrip('\r\n')
  n = n + 1
  rec = CFR(line,n)
  if n == 1:
   hrec = rec
   continue
  recsin.append(rec)
  d = rec.dict.upper()
  if d not in dictmap:
   dictmap[d] = []
  dictmap[d].append(rec)
 #print('check: dictmap keys=',dictmap.keys())
 f.close()

 # sort recsin in order of sorttime
 recs=sorted(recsin,key = lambda rec:rec.sorttime)
 # change 'n' based on sort order
 for j in range(0,len(recs)):
  rec = recs[j]
  out = "%s,%s,%s" %(rec.sorttime,rec.n,rec.lnum)
  rec.case = rec.n  # new
  rec.n = j+1
 knowndicts = ["AE","AP","AP90","BEN","BHS","BOR","BUR","CAE","CCS",
  "GRA","MW","MW72","PUI","PW","PWG",
  "SCH","SHS","SKD","STC","VCP","VEI","WIL","GST","PD","MD",
               "MCI","YAT","MWE","INM","IEG","PE","ACC","BOP","KRM","LAN",
               "LRV"]

 npending = generate_output("ALL",fileout,recs)
 print(n,"lines read from",filein)
 print(npending,"cases are pending")
 for d in dictmap:
  d = d.upper() # Jan 25, 2017
  if d not in knowndicts:
   out = "UNKNOWN DICTIONARY: %s %s" %(d,len(dictmap[d]))
   #print(out.encode('utf-8'))
   dmrecs = dictmap[d]
   print(len(dmrecs),"records for the unknown dictionary")
   dmrec = dmrecs[0]
   print('sorttime=',dmrec.sorttime)
   line = dmrec.line
   print('bad line=',line)
   m = len(recs)
   print("DBG: m=",m)
   for i in range(0,m):
    rec = recs[i]
    if rec.dict == d:
     outar=outputrec(rec,i)
     for out in outar:
      print(out.encode('utf-8'))
  else:
   generate_output(d,fileout,recs)

def init_recs(lines):
 recs = []
 for iline,line in enumerate(lines):
  n = iline + 1
  rec = CFR(line,n)
  recs.append(rec)
 return recs

def separate_recs(recs,option_string):
 a = [] # circle-recs
 b = [] # others
 for rec in recs:
  if option_string in rec.line:
   a.append(rec)
  else:
   b.append(rec)
 return a,b

def write_outrecs(fileout,outrecs):
 outarr = []
 for outrec in outrecs:
  for out in outrec:
   outarr.append(out)
 write_lines(fileout,outarr)
 
def parse_correction(rec):
 # return a list of strings
 outarr = outputrec(rec,"?????")
 return outarr

def  mark_mwlines(mwlines,recs1):
 d = {}
 for irec,rec in enumerate(recs1):
  L = rec.lnum
  # L may be duplicate
  if L not in d:
   d[L] = []
  d[L].append(irec+1)
 #
 newlines = []
 for iline,line in enumerate(mwlines):
  m = re.search(r'^<L>(.*?)<pc>(.*?)<',line)
  if m == None:
   newlines.append(line)
   continue
  # metaline
  L = m.group(1)
  pc = m.group(2)
  if L not in d:
   # no correction for this entry
   newlines.append(line)
   continue
  cases = d[L]  # list of correction cases
  cases1 = [str(case) for case in cases]
  cases_str = ','.join(cases1)
  pfx = '* case %s ' % cases_str
  # add a link to printed page
  href = 'http://localhost/cologne/csl-apidev/servepdf.php?dict=mw&page=%s' % pc
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
 filein = sys.argv[1]
 fileout = sys.argv[2]
 filein1 = sys.argv[3]  # copy of mw.txt
 fileout1 = sys.argv[4] # org-mode form, using also filein
 lines = read_lines(filein)
 recs = init_recs(lines)
 recs1 = sorted(recs, key = lambda rec: float(rec.lnum))
 # reset rec.n
 for irec,rec in enumerate(recs1):
  rec.n = irec + 1
 #for rec in recs1[:5]:
 # print(rec.lnum)
 #exit(1)
 # print(len(recs),"CFR records")
 outrecs = [parse_correction(rec) for rec in recs1]
 write_outrecs(fileout,outrecs)
 mwlines = read_lines(filein1)
 mwnewlines = mark_mwlines(mwlines,recs1)
 write_lines(fileout1,mwnewlines)
 # now 
