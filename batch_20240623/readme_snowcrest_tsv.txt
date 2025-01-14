
06-23-2024

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
