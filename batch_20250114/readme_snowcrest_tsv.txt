01-14-2025

----------------------
connect to cologne server.
git add .  #cfr.tsv
git commit -m "cfr.tsv on Cologne server since last commit"
git push  # push to github
----------------------
change to local installation of csl-corrections
git pull
# so now, local installation and cologne server are in sync

----------------------
Determine NEW lines of cfr.tsv to be processed
In local installation
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114

cat ../last_cfr_line.txt
 26030
# manually, check that line 26030 of cfr.tsv was processed
# and that line 26031 of cfr.tsv is not yet processed

sed '26030q;d' ../app/correction_response/cfr.tsv
10/06/2024 12:23:18     STC      15877  balāka  où les files de hérons passent. comme des sourires.     où les files de hérons passent comme des sourires.     Typo. But I think this translation is faulty, first it doesn't mean anything (at least for me), second, here hāsin doesn't mean "smiling at" but rather "dazzlingly white" and the whole compound would mean "dazzlingly white like a a flight of geese" and not "where lines of herons pass like smiles" (sic, but translated by Google)        Caujolle: corrected 10-09-2024

sed '26031q;d' ../app/correction_response/cfr.tsv

10/12/2024 09:45:54     SHS     7019    udāna   rises us        rises up       Typo     srhodes@snowcrest.net

So all lines starting with 26031 of cfr.tsv are NEW lines since latest
processing of cfr.tsv.

wc -l ../app/correction_response/cfr.tsv
 27195 ../app/correction_response/cfr.tsv

So lines 26031 through 27195 are NEW lines, to be processed.

-----------------------------------------------------------
(+ 26030 44)
python separate_scott.py 26030 ../app/correction_response/cfr.tsv tempprev.tsv scott.tsv notscott.tsv deleted.tsv
27195 lines read from ../app/correction_response/cfr.tsv
26030 lines written to tempprev.tsv
1003 lines written to scott.tsv
  Scott: SHS 212
  Scott: AP90 143
  Scott: MW 467
  Scott: LRV 180
  Scott: PUI 1
44 lines written to notscott.tsv
118 lines written to deleted.tsv

check: (+ 26030 1003 162) - 27195  

NOTE:
tempprev_cfr.tsv  lines 1-26030 of cfr.tsv
scott.tsv  subset of lines 26031-X and following that contain substring '\tsrhodes@snowcrest.net'
deleted.tsv new lines with no dictionary field  
notscott.tsv remaining new lines

------------------------------
# Manually examine deleted.tsv.
  If any line should be processed, insert that line at the proper time
  location into notscott.tsv


------------------------------
## get new cfr.tsv by concatenating tempprev_cfr.tsv AND notscott.tsv
cat tempprev.tsv notscott.tsv > ../app/correction_response/cfr.tsv

# check
wc -l ../app/correction_response/cfr.tsv
26074 ../app/correction_response/cfr.tsv

(+ 26030 44) == 26074

------------------------------
sync this repo to github, and then to Cologne
Note: It is possible that a user submitted a correction
  while the above work was done.
  So, on the Cologne server, check 'git status'

-----
On local server (at top level of csl-corrections repo)
git add .
git commit -m "Separate out Scott updates. See readme_snowcrest_tsv.txt in batch_20250114"
git push

-----
On Cologne server, cd to the csl-corrections directory
and git pull

***********************************************************
# Initialize the 'dictionaries' subdirectory
# Assume in batch_20250114
rm -r dictionaries  # remove previous 
mkdir dictionaries
# for each of Scott's dictionaries (see above list under separate_scott.py)
# make a subdirectory of dictionaries  (not lower case here)
mkdir dictionaries/shs
mkdir dictionaries/ap90
mkdir dictionaries/mw
mkdir dictionaries/lrv
mkdir dictionaries/pui

# generate dictionaries/xxx/xxx_correctionform.txt using scott.tsv

python3 ../cfr_adj.py scott.tsv correctionform.txt 
rewriting correctionform.txt ( 1002 pending )
1003 lines read from scott.tsv
1002 cases are pending
rewriting dictionaries/shs/shs_correctionform.txt ( 211 pending )
rewriting dictionaries/ap90/ap90_correctionform.txt ( 143 pending )
rewriting dictionaries/mw/mw_correctionform.txt ( 467 pending )
rewriting dictionaries/lrv/lrv_correctionform.txt ( 180 pending )
rewriting dictionaries/pui/pui_correctionform.txt ( 1 pending )



(+ 211 143 467 180 1) = 2002

Note: Why 'shs 211 pending'  BUT there are 212 lines in in scott.tsv
 with SHS dictionary?
 
***********************************************************
This ends the prepartion of Scott's corrections.
The task now is to process each of the
dictionaries/xxx/xxx_correctionform.txt files

***********************************************************
