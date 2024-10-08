

Process 1643 new lines in cfr.tsv
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/91

This local directory:
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

Start with cfr.tsv at commit 2c2451a4745d55077f201970c9d08594bd53d89c
cp ../cfr.tsv temp_cfr_0.tsv

First new line at line number 25995 '06/26/2024 11:41:36	PUI ...'
Separate temp_cfr_0.tsv into two files:
a. temp_cfr_1_newuser.tsv line#25995 and following  (1643 lines)
b. temp_cfr_1.tsv  First 25994 lines of temp_cfr_0.tsv

----------------------------
cp temp_cfr_1_newuser.tsv temp_cfr_1_newuser_a.tsv
Manual edit temp_cfr_1_newuser_a.tsv
Remove invalid/duplicate lines from temp_cfr_1_newuser_a.tsv  (114)
 1529 lines remain.
 (+ 1529 114) = 1643

1493 of these 1531 are from snowcrest (github user @aumsanskrit)
(- 1529 1493)  36 are from other users.


-----------------------------
Separate  temp_cfr_1_newuser_a.tsv into
a.  temp_cfr_1_scott.txt  (1493)
b.  temp_cfr_notscott.tsv (36)
There are some other duplicates to delete.

-----------------------------
temp_cfr_2.txt
  cat temp_cfr_1.tsv temp_cfr_notscott.tsv > temp_cfr_2.txt
-----------------------------

Replace cfr.tsv with temp_cfr_2.tsv --
  This has all the non-scott user corrections.
cp temp_cfr_2.tsv ../cfr.tsv

