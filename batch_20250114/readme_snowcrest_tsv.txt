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
OLD NOTES from ../batch_20240623/readme_snowcrest_tsv.txt -- to delete
ejf
THere is a backlog of user corrections from 01-26-2024 til now.
Most of these (690) of these are from user Scott.
The 'usual' method of handling these is unwieldy.

Thus separating out from cfr.tsv all of Scott's corrections into cfr_scott.tsv

These will be handled 'in batch' and the remaining to be handled in the usual way.

----------------------
Some stats:
last_cfr_line.txt = 25903  this is the line number of the last
line in cfr.tsv which is marked as handled (based on last field).

The line starts with 01/26/2024 11:26:13. 

The first 'not done' line is number 25904 01/26/2024 18:56:50
128 of lines at line number 25904 and following are 'srhodes'

211 lines match '.'  (i.e., there are 211 correction submissions in total,
       starting with line 25904.

So, (-211 128) = 83 correction submissions from other than srhodes.

------------------------------------
Update cfr.tsv and make cfr_snowcrest.tsv  (srhodes)
In emacs:
goto-line 25904
delete-non-matching-lines
 snowcrest
select these remaining lines into file cfr_snowcrest.tsv
undo (this restores cfr.tsv)
----
# now delete the snowcrest lines in cfr.tsv
goto-line 25904
delete-matching-lines  (snowcrest)
save cfr.tsv

--------------------------------------------
cd csl-corrections
git add .  # cfr.tsv, cfr_snowcrest.tsv
git commit -m "snowcrest batch corrections"
git push
--------------
## login to cologne and git pull csl-corrections

--------------------------------------------
at top-level of csl-corrections:

mkdir temp_batch1
cd temp_batch1
cp ../app/correction_response/cfr_snowcrest.tsv .

python3 ../cfr_adj.py cfr_snowcrest.tsv correctionform.txt 

ERROR: Missing directory dictionaries/shs
mkdir dictionaries
mkdir dictionaries/shs

mkdir dictionaries/mw
mkdir dictionaries/ap90
mkdir dictionaries/pui

rewriting correctionform.txt ( 689 pending )
690 lines read from cfr_scott.tsv
689 cases are pending
dictionaries/shs/shs_correctionform.txt ( 64 pending )
rewriting dictionaries/mw/mw_correctionform.txt ( 603 pending )
rewriting dictionaries/ap90/ap90_correctionform.txt ( 19 pending )
rewriting dictionaries/pui/pui_correctionform.txt ( 3 pending )


Now for the batch correction work.
