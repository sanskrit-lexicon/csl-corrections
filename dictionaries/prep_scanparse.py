""" With VEI, Sampada changed format for indicating scan errors.
Namely, put ':scan error' at the end of lines
This program changes such to be consistent with what scanparse.py expects.
It changes 
L:k1:word:correction:scan error
to two lines:
L:k1:word:correction
; scan error

"""
import sys,re,codecs

def adjust_lines(lines):
 ans = []
 for line in lines:
  if line.startswith(';'):
   ans.append(line)
   continue
  parts = line.split(':')
  if (len(parts) == 5) and (parts[-1].strip() == 'scan error'):
   a = ':'.join(parts[:4])
   ans.append(a)
   ans.append('; scan error')
  elif (len(parts) == 5):
   a = ':'.join(parts[:4])
   ans.append(a)
   ans.append('; %s' % parts[-1])
   
  else:
   ans.append(line)
 return ans

if __name__ == "__main__":
 try:
  filein = sys.argv[1]
  fileout = sys.argv[2]
 except:
  print('Usage: python prep_scanparse.py xxx_error.txt xxx_error1.txt')
  exit(1)
 with codecs.open(filein,"r","utf-8") as f:
  lines = [x.rstrip('\r\n') for x in f]
  print(len(lines),"lines read from",filein)
 newlines = adjust_lines(lines)
 print(len(newlines),"lines written to",fileout)
 with codecs.open(fileout,"w","utf-8") as f:
  for line in newlines:
   f.write(line+'\n')

