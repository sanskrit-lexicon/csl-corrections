# coding=utf-8
""" make_change_abbrev.py
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
 for c in changes:
  outarr = []
  outarr.append('; -----------------------------------------------------')
  outarr.append('; %s' %c.metaline)
  for rep in c.replacements:
   outarr.append('; oldls:%s' % rep.old)
   outarr.append('; newls:%s' % rep.new)
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
 def __init__(self,oldline,newline,metaline,replacements,lnum):
  # a -> b
  self.oldline = oldline
  self.newline = newline
  self.lnum = lnum
  self.metaline = metaline
  self.replacements = replacements

def generate_groups(lines):
 group = None
 for iline,line in enumerate(lines):
  m = re.search(r'^[*] +(<ls.*?</ls>)$',line)
  if m != None:
   group = [m.group(1)]
   continue
  if line == '':
   yield group
   group = None
   continue
  m = re.search(r'(<ls.*?</ls>)',line)
  if m == None:
   print('generate_groups error at line %s: %s' %(iline+1,line))
   exit(1)
  group.append(m.group(1))

class Replacement:
 def __init__(self,old,new):
  self.old = old
  self.new = new
  self.count = 0
  
def init_replacements(filein):
 lines = read_lines(filein)
 groups = list(generate_groups(lines))
 print("init_replacements: %s groups" % len(groups))
 reps = []
 d = {}
 for group in groups:
  old = group[0]
  new = ' '.join(group[1:])
  rep = Replacement(old,new)
  if old in d:
   print('init_replacements skipping duplicate',old)
   continue
  reps.append(rep)
  d[old] = rep
 return reps,d

def get_newline(line,drec):
 dbg = False
 if dbg: print(line)
 lsarr = re.findall(r'<ls.*?</ls>',line)
 replacements = []
 for ls in lsarr:
  if ls not in drec:
   continue
  replacements.append(drec[ls])
  drec[ls].count = drec[ls].count + 1
 if replacements == []:
  return line,replacements
 # generate newline
 newline = line
 for rep in replacements:
  old = rep.old
  new = rep.new
  newline = newline.replace(old,new)
 return newline,replacements

def get_changes_lnum():
 lnums = [
20650, 22887, 24433, 24917, 28985, 
28988, 28991, 29003, 29006, 52297, 
52732, 65373, 67832, 70822, 71050, 
71077, 71110, 71170, 71200, 71227, 
71230, 71260, 71299, 71302, 71347, 
71437, 71470, 71503, 71542, 71662, 
71755, 71845, 73351, 73756, 80526, 
80532, 84531, 97222, 101070, 101118, 
112340, 113663, 113952, 154035, 183440, 
183452, 183569, 184339, 208422, 212264, 
213365, 222503, 223193, 235769, 261472, 
267495, 269191, 269251, 278734, 278815, 
282766, 293847, 403673, 490078, 493990,
575172, 604171, 604183, 619447, 691555,
708114, 708117, 764030, 795097, 798931,
833593, 854131, 859065, 
 ]
 s = set(lnums)
 return s

changes_lnum = get_changes_lnum()

def make_changes(entries):
 changes = []
 for ientry,e in enumerate(entries):
  for iline,line in enumerate(e.datalines):
   metaline = e.metaline
   lnum = e.linenum1 + iline + 1
   if lnum in changes_lnum:
    newline = line
    replacements = []
    change = Change(line,newline,metaline,replacements,lnum)
    changes.append(change)
 return changes

def check_reps(reps):
 n = 0 # total count of rep.count
 for rep in reps:
  n = n + rep.count
  if rep.count == 0:
   print('not used:',rep.old)
 print(n,'count of replacements')
 
if __name__=="__main__":
 filein = sys.argv[1]  # xxx.txt
 fileout = sys.argv[2] # change transactions
 entries = digentry.init(filein)

 changes = make_changes(entries)
 print(len(changes),"lines changes")
 write_changes(fileout,changes)

