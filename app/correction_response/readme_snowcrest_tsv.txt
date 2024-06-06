05-29-2024
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

------------------------------
603 of these are '\tmw\t.*snowcrest'  (or MW)
625 of these are '\tmw\t'  (or MW)
691 of these mare snowcrest.net

wc -l cfr.tsv
26668 cfr.tsv

delete all 'snowcrest' lines (starting at line number 25904)
and move these into cfr_snowcrest.tsv
wc -l cfr_snowcrest.tsv
690 cfr_snowcrest.tsv

wc -l cfr.tsv
25978 cfr.tsv

(+ 25978 690)
26668

----------------------------------------------------
at top-level of csl-corrections:

mkdir temp_batch
cd temp_batch
cp ../app/correction_response/cfr_scott.tsv .

python3 ../cfr_adj.py cfr_scott.tsv correctionform.txt 

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
