csl-corrections/batches/20251126

How to separate Scott's submissions from the others.

----------------------
connect to cologne server.

Edit cfr.tsv on server, removing ill-formed entries.
 (csl-corrections/app/correction_response/cfr.tsv
git add .  #cfr.tsv
git commit -m "Remove records with only date"
git push  # push to github
----------------------
#change to local installation of csl-corrections
cd /c/xampp/htdocs/cologne/csl-corrections/
git pull
# so now, local installation and cologne server are in sync
The last line of cfr.tsv now starts with
11/26/2025 09:23:15  SHS 21095

----------------------
# Save a not-tracked copy of cfr.tsv, just for safety
cd /c/xampp/htdocs/cologne/csl-corrections
cd app/correction_response
cp cfr.tsv temp_cfr_20251126_before.tsv
cd /c/xampp/htdocs/cologne/csl-corrections

----------------------
# make directory for new batch
cd /c/xampp/htdocs/cologne/csl-corrections/batches
mkdir 20251126
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126

----------------------
previous batch:
cd csl-corrections/batch_20250418  
 tail -n 1 scott.tsv
   04/18/2025 21:09:34
 
 tail -n 1 notscott.tsv 
   04/17/2025 12:34:45   (date time used below in separate_scott1.py
   '20250417 12:34:45' # parameter used by 
  
------------------------

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126
separate_scott2.py is a variant of
  ../../batch_20250114/separate_scott.py 

# edit separate_scott2.py to read first parameter as 'yyyymmdd hh:mm:ss'
# The program only deals with lines of cfr.tsv
# whose date is GREATER THAN yyyymmdd of previous batch (see above)
#  
# Use date of the batch last line of notscott.tsv in previous batch
date previous to 20251126 is 20250417

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126
python separate_scott2.py '20250417 12:34:45' ../../app/correction_response/cfr.tsv prev.tsv scott.tsv notscott.tsv deleted.tsv

The first
--- results:
28558 lines read from ../../app/correction_response/cfr.tsv
26113 lines written to prev.tsv
2357 lines written to scott.tsv
  Scott: LRV 179
  Scott: AP 1612
  Scott: MW 316
  Scott: SHS 223
  Scott: PW 26
  Scott: VCP 1
88 lines written to notscott.tsv
0 lines written to deleted.tsv

(+ 26113 2357 88 0) 28558 AS EXPECTED

---------------------------------------
# construct new cfr.tsv
  as concatenation of prev.tsv and notscott.tsv\
cat prev.tsv notscott.tsv > new_cfr.tsv

# replace production cfr.tsv with new_cfr.tsv
cp new_cfr.tsv ../../app/correction_response/cfr.tsv

--------------------------------
INSTALLATION of revised cfr.tsv
----
# sync cfr.tsv to github
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response
git status
git add .
git commit -m "revise cfr.tsv to batches/20251126/new_cfr.tsv"
git push

# sync cologne to github

On cologne server,
cd csl-corrections and pull
git pull

#  app/correction_response/cfr.tsv
# 1 file changed, 2357 deletions(-)

Now local, github, and cologne are synced.


***********************************************************
# Initialize the 'dictionaries' subdirectory in batches/20251126

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126

mkdir dictionaries
# for each of Scott's dictionaries (see above list)
# make a subdirectory of dictionaries 
mkdir dictionaries/lrv
mkdir dictionaries/ap
mkdir dictionaries/mw
mkdir dictionaries/shs
mkdir dictionaries/pw
mkdir dictionaries/vcp

# generate dictionaries/xxx/xxx_correctionform.txt using scott.tsv

python3 ../../cfr_adj.py scott.tsv correctionform.txt

--- results:
rewriting correctionform.txt ( 2356 pending )
2357 lines read from scott.tsv
2356 cases are pending
rewriting dictionaries/lrv/lrv_correctionform.txt ( 178 pending )
rewriting dictionaries/ap/ap_correctionform.txt ( 1612 pending )
rewriting dictionaries/mw/mw_correctionform.txt ( 316 pending )
rewriting dictionaries/shs/shs_correctionform.txt ( 223 pending )
rewriting dictionaries/pw/pw_correctionform.txt ( 26 pending )
rewriting dictionaries/vcp/vcp_correctionform.txt ( 1 pending )

***********************************************************
This ends the preparation of Scott's corrections as of 20251126
The task now is to process each of the
dictionaries/xxx/xxx_correctionform.txt files

# push to github 
cd /c/xampp/htdocs/cologne/csl-corrections
git add .
git commit -m "construct dictionaries directory of batch_20251126"
git push

***********************************************************
11/26/2025 Begin corrections to MW.
See readme.txt in batches/20251126/dictionaries/mw

  
***********************************************************
11/26/2025  THE FOLLOWING STEPS NOT (YET) DONE
***********************************************************
Handling of the notscott.tsv items
These are now part of the "regular' system.

cd /c/xampp/htdocs/cologne/csl-corrections
# update dictionaries/xxx/xxx_correctionform.txt 
sh redo_cfr.sh

--- Results
regenerate correctionform.txt and dictionaries/xxx/xxx_correctionform.txt
rewriting correctionform.txt ( 83 pending )
26113 lines read from app/correction_response/cfr.tsv
83 cases are pending
dictionaries/skd/skd_correctionform.txt ( 1 pending )
rewriting dictionaries/vcp/vcp_correctionform.txt ( 1 pending )
dictionaries/pwg/pwg_correctionform.txt ( 1 pending )
rewriting dictionaries/mw/mw_correctionform.txt ( 23 pending )
rewriting dictionaries/shs/shs_correctionform.txt ( 14 pending )
rewriting dictionaries/bur/bur_correctionform.txt ( 3 pending )
rewriting dictionaries/pw/pw_correctionform.txt ( 3 pending )
rewriting dictionaries/gra/gra_correctionform.txt ( 2 pending )
rewriting dictionaries/ap90/ap90_correctionform.txt ( 2 pending )
dictionaries/gst/gst_correctionform.txt ( 1 pending )
dictionaries/md/md_correctionform.txt ( 2 pending )
dictionaries/mwe/mwe_correctionform.txt ( 1 pending )
rewriting dictionaries/ap/ap_correctionform.txt ( 28 pending )
rewriting dictionaries/ieg/ieg_correctionform.txt ( 1 pending )
redo_cfr.sh is finished

------------------------------------------
preparing issues in csl-orig.
This requires github access token.
See readme_howto.txt for how to get one (with an expiration).

---
cat last_cfr_line.txt
26074

This means that line 26074 of cfr.tsv was the last in cfr.tsv that
has been posted to github csl-orig/issues.

The last line in cfr.tsv is currently line number 26113.
(- 26113 26074) 39  new ones to post issues.

39 issues uploaded  last_cfr_line.txt was changed.
cat last_cfr_line.txt
26113

This expected.

Sync to github and cologne.

git add .
git commit -m "non-scott user corrections prepared.
See end of file batch_20251126/readme_batch_20251126.txt"
git push

At colonge csl-corrections, git pull.

