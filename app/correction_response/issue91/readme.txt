

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

Synced the revised cfr.tsv with Github and cologne server.
commit: 2e1973dd378b9f84047939c166ab4ef19d6638f6
-----------------------------
10-10-2024
Added new corrections 10-09/10-10 to temp_cfr_1_scott.txt
These lines are in temp_10_10_scottextra.txt.
First is 10/09/2024 05:46:57
Last  is 10/10/2024 17:33:54
-----------------------------
now at commit 784cab8af458dab7a63511ed33d727351232034f of csl-corrections.
-----------------------------
10-11-2024

"double"  "Double Indentation Error"
"Al

python separate.py double temp_cfr_1_scott.txt temp_cfr_1_scott_double.txt temp_cfr_1_scott_not_double.txt
1518 lines read from temp_cfr_1_scott.txt
1518 CFR records
573 lines written to temp_cfr_1_scott_double.txt
945 lines written to temp_cfr_1_scott_not_double.txt

python separate.py alpha temp_cfr_1_scott_not_double.txt temp_cfr_1_scott_alpha.txt temp_cfr_1_scott_not_alpha.txt

938 lines read from temp_cfr_1_scott_not_double.txt
938 CFR records
38 lines written to temp_cfr_1_scott_alpha.txt
900 lines written to temp_cfr_1_scott_not_alpha.txt

python separate.py insert temp_cfr_1_scott_not_alpha.txt temp_cfr_1_scott_insert.txt temp_cfr_1_scott_not_insert.txt
900 lines read from temp_cfr_1_scott_not_alpha.txt
900 CFR records
162 lines written to temp_cfr_1_scott_insert.txt
738 lines written to temp_cfr_1_scott_not_insert.txt

python separate.py mw temp_cfr_1_scott_not_insert.txt temp_cfr_1_scott_mw.txt temp_cfr_1_scott_not_mw.txt

738 lines read from temp_cfr_1_scott_not_insert.txt
738 CFR records
674 lines written to temp_cfr_1_scott_mw.txt
64 lines written to temp_cfr_1_scott_not_mw.txt

python separate.py ap90 temp_cfr_1_scott_not_mw.txt temp_cfr_1_scott_ap90.txt temp_cfr_1_scott_not_ap90.txt
64 lines read from temp_cfr_1_scott_not_mw.txt
64 CFR records
22 lines written to temp_cfr_1_scott_ap90.txt
42 lines written to temp_cfr_1_scott_not_ap90.txt

python separate.py shs temp_cfr_1_scott_not_ap90.txt temp_cfr_1_scott_shs.txt temp_cfr_1_scott_not_shs.txt

42 lines read from temp_cfr_1_scott_not_ap90.txt
42 CFR records
35 lines written to temp_cfr_1_scott_shs.txt
7 lines written to temp_cfr_1_scott_not_shs.txt

python separate.py pui temp_cfr_1_scott_not_shs.txt temp_cfr_1_scott_pui.txt temp_cfr_1_scott_not_pui.txt
7 lines read from temp_cfr_1_scott_not_shs.txt
7 CFR records
5 lines written to temp_cfr_1_scott_pui.txt
2 lines written to temp_cfr_1_scott_not_pui.txt

cp temp_cfr_1_scott_not_pui.txt temp_cfr_1_scott_lrv.txt

--------------------------------------------------------
Process the 64 non-MW records, by dictionary: lrv, shs, pui, ap90

python parse_corrections.py temp_cfr_1_scott_lrv.txt corrections_lrv.txt
--------------------------------------------------------
temp_cfr_extra_20241011.txt
  records removed from cologne cfr.tsv dated 10/11/2024
Sync this csl-corrections repo to github
Then sync to Cologne
--------------------------
python parse_corrections.py temp_cfr_1_scott_shs.txt corrections_shs.txt

35 lines read from temp_cfr_1_scott_shs.txt

edit /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt
and corrections_shs.txt.

sync csl-orig to github
sync Cologne to github
-------------------------
python parse_corrections.py temp_cfr_1_scott_pui.txt corrections_pui.txt
5 lines read from temp_cfr_1_scott_pui.txt

edit /c/xampp/htdocs/cologne/csl-orig/v02/pui/pui.txt
and corrections_pui.txt

cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh pui  ../../pui
sh xmlchk_xampp.sh pui
# ok  No problems noticed
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

push to github
cd /c/xampp/htdocs/cologne/csl-orig
git add .
git commit -m "PUI: See corrections_pui.txt at
Ref https://github.com/sanskrit-lexicon/csl-corrections/issues/91"
git push
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

sync csl-orig at Cologne, and regenerate pui displays at Cologne.

sync this csl-corrections repo to Github and cologne.

--------------------------
# add some corrections of 10/12/2024 to temp_cfr_1_scott_ap90.txt
python parse_corrections.py temp_cfr_1_scott_ap90.txt corrections_ap90.txt
27 lines read from temp_cfr_1_scott_ap90.txt

edit /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
and corrections_ap90.txt

installation ...

cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
# ok  No problems noticed
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

# push csl-orig to github
cd /c/xampp/htdocs/cologne/csl-orig
git add .
git commit -m "AP90: See corrections_ap90.txt at
Ref https://github.com/sanskrit-lexicon/csl-corrections/issues/91"
git push
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

# push csl-pywork to github
cd /c/xampp/htdocs/cologne/csl-pywork
git add .
git commit -m "AP90: ap90ab revised"
git push
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

sync csl-orig and csl-pywork at Cologne.
regenerate ap90 displays at Cologne.

sync this csl-corrections repo to Github and cologne.
-----------------------------------------------------
