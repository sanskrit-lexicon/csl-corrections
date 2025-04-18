04-18-2025
How to separate Scott's submissions from the others.

----------------------
connect to cologne server.

Edit cfr.tsv on server, removing ill-formed entries.

git add .  #cfr.tsv
git commit -m "cfr.tsv on Cologne server since last commit"
git push  # push to github
----------------------
change to local installation of csl-corrections
git pull
# so now, local installation and cologne server are in sync
----------------------
# Save a local copy of cfr.tsv, just for safety
cd /c/xampp/htdocs/cologne/csl-corrections
cd app/correction_response
cp cfr.tsv cfr_20250418_before.tsv
cd /c/xampp/htdocs/cologne/csl-corrections

----------------------
# make directory for new batch
cd /c/xampp/htdocs/cologne/csl-corrections
mkdir batch_20250418

----------------------
previous batch_20250114
 scott.tsv    01/14/2025 13:05:48 last
 notscott.tsv 01/13/2025 20:44:09 last

conclude:  Generate (in batch_20250418)


cp ../batch_20250114/separate_scott.py separate_scott1.py

# edit separate_scott1.py to read first parameter as yyyymmdd
# The program only deals with lines of cfr.tsv
# whose date is GREATER THAN yyyymmdd

python separate_scott1.py 20250114 ../app/correction_response/cfr.tsv prev.tsv scott.tsv notscott.tsv deleted.tsv

--- results:
27451 lines read from ../app/correction_response/cfr.tsv
26074 lines written to prev.tsv
1336 lines written to scott.tsv
  Scott: LRV 279
  Scott: MW 190
  Scott: SHS 222
  Scott: AP90 42
  Scott: AP 602
  Scott: PUI 1
41 lines written to notscott.tsv
0 lines written to deleted.tsv

(+ 26074 1336 41) = 27451  AS EXPECTED
xxx
---------------------------------------
# construct new cfr.tsv
  as concatenation of prev.tsv and notscott.tsv
cat prev.tsv notscott.tsv > new_cfr.tsv

cp new_cfr.tsv ../app/correction_response/cfr.tsv

----
# sync cfr.tsv to github
cd /c/xampp/htdocs/cologne/csl-corrections
git status
git add .
git commit -m "revise cfr.tsv to batch_20251418/new_cfr.tsv"
git push
# sync cologne to github
On cologne server,
git pull

Now local, github, and cologne are synced.



***********************************************************
# Initialize the 'dictionaries' subdirectory
# Assume in batch_20250418
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418

mkdir dictionaries
# for each of Scott's dictionaries (see above list under separate_scott.py)
# make a subdirectory of dictionaries 
mkdir dictionaries/lrv
mkdir dictionaries/mw
mkdir dictionaries/shs
mkdir dictionaries/ap90
mkdir dictionaries/ap
mkdir dictionaries/pui

# generate dictionaries/xxx/xxx_correctionform.txt using scott.tsv

python3 ../cfr_adj.py scott.tsv correctionform.txt

--- results:
rewriting correctionform.txt ( 1335 pending )
1336 lines read from scott.tsv
1335 cases are pending
rewriting dictionaries/lrv/lrv_correctionform.txt ( 278 pending )
rewriting dictionaries/mw/mw_correctionform.txt ( 190 pending )
rewriting dictionaries/shs/shs_correctionform.txt ( 222 pending )
rewriting dictionaries/ap90/ap90_correctionform.txt ( 42 pending )
rewriting dictionaries/ap/ap_correctionform.txt ( 602 pending )
rewriting dictionaries/pui/pui_correctionform.txt ( 1 pending )

***********************************************************
This ends the preparation of Scott's corrections ast of 20250418
The task now is to process each of the
dictionaries/xxx/xxx_correctionform.txt files

# push to github 
cd /c/xampp/htdocs/cologne/csl-corrections
git add .
git commit -m "construct dictionaries directory of batch_20250418"
git push

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
See end of file batch_20250418/readme_batch_20250418.txt"
git push

At colonge csl-corrections, git pull.

