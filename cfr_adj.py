""" cfr_adj.py  Sep 29, 2014
 Oct 17, 2014: Separate collations by dictionary
funderburkjim@gmail.com Oct 18, 2014: Use 'dictionaries' subdirectory. 
      Put correction forms in dictionaries/X/ directory
 Usage: python cfr_adj.py cfr.tsv correctionform.txt
  Note: cfr.tsv is created from Google Spreadsheet
        'Sanskrit-Lexicon Correction form (Responses)'
        by 'File/Download as tab-separated values'
 Jul 18, 2015  Sort records by time, since Google doesn't append
   new records from Correction form to the end.
 Aug 2, 2015  Correct construction of sorttime.
 Dec 17, 2019 python3 compatible
 Dec 17, 2019 check_for_new function. Thus, if no new corrections for
    a given dictionary xxx, then dictionaries/xxx/xxx_correctionform.txt is
    not changed.
 Apr 06, 2026 Check for occurrence of 'Which Dictionary?' to decide whether there 
     is a header or not. If header, skip it. Otherwise, process all lines.
 Sep 02, 2026 (H3885) Two guards, because this file's output is committed to a
     PUBLIC repository by a nightly cron:
     (a) validate_tsv() refuses to write anything unless EVERY data line has
         exactly 8 tab-parts -- a 404 HTML page saved by the fetch job used to
         reach this script and die halfway through;
     (b) the e-mail column is pseudonymised in place (cfr_email_mask) before a
         single line is parsed, so daily/ TSVs and everything derived from them
         never carry an address.
"""
from __future__ import print_function
import re,sys,os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cfr_email_mask import mask_tsv_file  # noqa: E402

def oneline(x):
 parts = re.split(r'[\r\n]',x)
 y = ' '.join(parts)
 return y

class CFRShapeError(Exception):
 """ A data line does not have the 8 tab-parts the correction form produces. """
 def __init__(self,n,nparts):
  self.n = n
  self.nparts = nparts
  msg = "line %s: # of tab-parts should be 8, but is %s" % (n,nparts)
  Exception.__init__(self,msg)

def validate_tsv(filein):
 """ Refuse the file unless every data line has exactly 8 tab-parts.

     The fetch job once saved a 404 HTML page under the .tsv name; parsing it
     half-way rewrote correctionform files from garbage.  Nothing is written
     until this passes.  Returns the number of data lines.
 """
 problems = []
 ndata = 0
 with open(filein,'r') as f:
  for n,line in enumerate(f,start=1):
   line = line.rstrip('\r\n')
   if n == 1 and 'Which Dictionary?' in line:
    continue  # header
   if line.strip() == '':
    continue
   ndata = ndata + 1
   nparts = len(line.split('\t'))
   if nparts != 8:
    problems.append((n,nparts))
 if problems:
  print("ERROR: %s is not a correction-form TSV." % filein, file=sys.stderr)
  for n,nparts in problems[:5]:
   print("  line %s has %s tab-parts, expected 8" % (n,nparts), file=sys.stderr)
  if len(problems) > 5:
   print("  ... and %s more bad line(s)" % (len(problems)-5), file=sys.stderr)
  print("Refusing to write any output.", file=sys.stderr)
  sys.exit(1)
 if ndata == 0:
  print("ERROR: %s has no data lines. Refusing to write any output." % filein,
        file=sys.stderr)
  sys.exit(1)
 return ndata

class CFR(object):
 def __init__(self,line,n):
  parts = line.split('\t')
  self.line = line
  self.n = n
  if len(parts)!= 8:
   # Should be unreachable: validate_tsv() rejects the file before we get here.
   raise CFRShapeError(n, len(parts))
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
   os.makedirs(dir)
   print("CREATED directory %s" % dir)
 if dcode != 'ALL':
  write_flag = check_for_new(allarr,fileout)
 else: # always rewrite the global correctionform.txt file
  write_flag = True
 if write_flag:
  print('rewriting',fileout,'(',npending,'pending )')
  fout = open(fileout,'w')
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
 with open(fileout,"r") as f:
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
 f = open(filein,'r')
 n = 0
 recsin = []
 dictmap = {}
 first_line = True
 for line in f:
  line = line.rstrip('\r\n')
  n = n + 1
  if first_line:
   first_line = False
   if 'Which Dictionary?' in line:
    continue  # skip header line
  rec = CFR(line,n)
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
               "LRV","FRI"]

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

#-----------------------------------------------------
if __name__=="__main__":
 filein = sys.argv[1]
 fileout = sys.argv[2]
 ndata = validate_tsv(filein)
 print("%s: %s data line(s), 8 tab-parts each" % (filein,ndata))
 nmasked = mask_tsv_file(filein)
 print("e-mail column pseudonymised in %s line(s) of %s" % (nmasked,filein))
 adjust(filein,fileout)
