

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

separate.py splits a file into two pieces, based on a string match:.
These are applied in order.

 "double": "Double Indentation Error",
 "alpha": "Alphabetical Placement Error",
 "insert": "Supplemental Insertion",
 "mw": "MW",
 "ap90": "AP90",
 "shs": "SHS",
 "pui": "PUI",
 "abbrev" : "°",  # mostly non-standard local abbreviations
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
Begin processing of the MW records.
Recall they are in separate files:
First, we tackle temp_cfr_1_scott_mw.txt 674 entries

python separate.py abbrev temp_cfr_1_scott_mw.txt temp_cfr_1_scott_mw_abbrev.txt temp_cfr_1_scott_mw_not_abbrev.txt
674 lines read from temp_cfr_1_scott_mw.txt
674 CFR records
119 lines written to temp_cfr_1_scott_mw_abbrev.txt
555 lines written to temp_cfr_1_scott_mw_not_abbrev.txt

------------------------------------------
python parse_corrections.py temp_cfr_1_scott_mw_abbrev.txt corrections_mw_abbrev.txt
edit temp_cfr_1_scott_mw_abbrev.txt and
csl-orig/v02/mw/mw.txt

TODO
----
See case 5 in corrections_mw_abbrev
-°  -> ? °
7259 matches in 7217 lines for "<s>[^<]*-°" in buffer: mw.txt
----
Similar:
Example L=114503: <s>pawwi—lo°Draka</s>
4605 matches in 4562 lines for "<s>[^<]*—[^<]*°"
----
Similar: -°
Example:  case 18 197587 vipaTAvapAtaparatA
13700 matches in 13024 lines for "<s>[^<]*-[^<]*°" in buffer: mw.txt
----
Examples under Case 24 vigatoddhava
if there is no number "1", then the number "2"
Good idea to find similar problems where a homonym number for vigata was erroneously
inserted by cdsl into the compounds of vigata.
----
Another example : vigraha cpds.
----
768 matches in 766 lines for "</s> <ab>g.</ab>"
 Should all these be changed to "</s>, <ab>g.</ab>"  (comma)?
 (Case 97)
----


installation of mw

cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok  No problems noticed
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

# push csl-orig to github
cd /c/xampp/htdocs/cologne/csl-orig
git add .
git commit -m "MW: See corrections_mw_abbrev.txt at
Ref https://github.com/sanskrit-lexicon/csl-corrections/issues/91"
git push
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

sync csl-orig and csl-pywork at Cologne.
regenerate ap90 displays at Cologne.

# update mw_printchange.txt

# Sync this csl-corrections repo with github and Cologne.
-------------------------------------------------------------------
10-14-2024
temp_cfr_1_scott_mw_not_abbrev.txt

There are 9 non-MW corrections here.
Remove these to temp_cfr_1_scott_misc1.txt.

--------------------------------------------------------
temp_cfr_1_scott_mw_not_abbrev.txt has 546 items.
This is a large number for manual checking.
Make a special form of corrections, ordered by Lnum.
Also temporary markup to a copy of mw.txt for edit efficiency

cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt
Remove blanks at end of lines.  87 occurrences
python parse_corrections1.py temp_cfr_1_scott_mw_not_abbrev.txt corrections_mw_not_abbrev.txt temp_mw_0.txt temp_mw_0_work.txt

python remove_markup.py temp_mw_0_work.txt temp_mw_1.txt

# local install temp_mw_1.txt
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok  No problems noticed
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

sh temp_redo_1.sh  (does the steps above in a script)
-----
TODO
----
dangling id. references  Example is Case 2.
  cdsl has no syntax for 'id.' references.
----
<s>gezam</s> See <s>anu-</s>  -> <s>gezam</s>, see <s>anu-</s>

Possible global change: "</s> See <s>" -> "</s>, see <s>"
----
|’ <ab>cf.</ab>| -> |’, <ab>cf.</ab>|  possible global chg.
7 matches for "’, <ab>cf.</ab>"
37 matches for "’ <ab>cf.</ab>"
----
' = prec.' in supplement entries. See Case 141 चीवरवत् for discussion.
---
old = jarījṛmbhate
new = jarījṛmbhyate
Case 162  intensive form question
-------------------------
Change 'phw' (parenthetical headword) markup to 'Alternate headword'
markup. Example:
OLD:
<L>105760<pc>536,1<k1>nAmaDeya<k2>nAma—De/ya<e>3
<s>nAma—De/ya</s> ¦ <lex>n.</lex> a name, title, appellation (often <ab>ifc.</ab>; <ab>cf.</ab> <s>kiM-n°</s>, <s>puM-n°</s> &c.), <ls>RV.</ls> &c. &c.<info lex="n"/>
<LEND>
<L>105761<pc>536,1<k1>nAmaDeya<k2>nAma—De/ya<e>3A
¦ the ceremony of giving a name to a child, <ls>Mn. ii, 123</ls> (also <s>-karaRa</s> <lex type="phw">n.</lex> the ceremony of giving a name to a child, <ls>Gobh.</ls>)<info lex="inh"/>
<LEND>
<L>105761.01<pc>536,1<k1>nAmaDeyakaraRa<k2>nAma—Deya—karaRa<e>4
<s>nAma—Deya—karaRa</s> ¦ <lex>n.</lex>, <ls>Gobh.</ls><info phwparent="105761,nAmaDeya"/><info lex="n"/>
<LEND>
-----------------

NEW:
<L>105760<pc>536,1<k1>nAmaDeya<k2>nAma—De/ya<e>3
<s>nAma—De/ya</s> ¦ <lex>n.</lex> a name, title, appellation (often <ab>ifc.</ab>; <ab>cf.</ab> <s>kiM-n°</s>, <s>puM-n°</s> &c.), <ls>RV.</ls> &c. &c.<info lex="n"/>
<div n="1"/> the ceremony of giving a name to a child, <ls>Mn. ii, 123</ls> (also <s>-karaRa</s> <lex type="phw">n.</lex> <ls>Gobh.</ls>)<info lex="inh"/>
<LEND>
<L>105760.1<pc>536,1<k1>nAmaDeyakaraRa<k2>nAma—Deya—karaRa<e>4
{{Lbody=105760}}
<LEND>
====
pratyayas vs compounds  H3 -> H2?
Example case 256:
nikam H1, nikAma H3, nikAma-kAma H4.
  An interesting question: should it be nikAma H2 ?
  If so, then nikAma-kAma would be H3.
----
ref case 270 netrasaMkocana
Sanskrit alphabetical order.
----
<ab>v.l.</ab> for <ab>prec.</ab>  L=183462 lokasmft
 'prec.' (preceding) is ambiguous in digital edition,
   similar to dangling 'id.
----
 Erroneous 'carrying over' of homonym number to sub-headwords.
 See Scott's discussion under case 388.
 Scott has found several of these.
 Can we find some (programmatic) way to identify any other such
 errors lurking in mw.txt?
----
 Revision Symbol Missing
 Example: Case 392 194978, hw=vijāman
 The Circle is missing for a technical reason,
  somehow related to:
  L=193039  no rev
  L=194978  rev
 The rev-sup circles in left pane of list display
 are computed 'on the fly' by the list display.
 First it gathers the list (the specific L-numbers)
 Then  it assigns circle based on presence
 of <info n="rev"../> or <info n="sup"/> in the
 specific entries comprising the list.
 But when the initial list is computed,  duplicates
  are skipped. So our 194978 is NOT in the list,
  since it is viewed as a duplicate.
  Only 193039 is in the list, and it has no 'rev'
  markup.

 
--------------------------------------------------------
syntax of '<chg>' element.
<chg type="chg" n="1" src="mw"><old></old><new></new></chg>
--------------------------------------------------------

10-19-2024
install corrections from corrections_mw_not_abbrev.txt

# local install temp_mw_1.txt
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok  No problems noticed
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

push to github
cd /c/xampp/htdocs/cologne/csl-orig
git add .
git commit -m "MW: See corrections_mw_not_abbrev.txt at
Ref https://github.com/sanskrit-lexicon/csl-corrections/issues/91"
git push
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91
----------------------------
sync csl-orig at Cologne, and regenerate mw displays at Cologne.

----------------------------

sync this csl-corrections repo to Github and cologne.

This finishes Jim's work on corrections_mw_not_abbrev.txt
--------------------------------------------------------
10-20-2024
More wrongly marked abbreviations using °
Manual Emacs work derived a list of line-numbers with these texts.
Next program makes prototype change records
python make_change_abbrev.py temp_mw_1.txt changes_abbrev.txt
# manual edit changes_abbrev.txt

python updateByLine.py temp_mw_1.txt changes_abbrev.txt temp_mw_2.txt
877277 lines read from temp_mw_1.txt
877277 records written to temp_mw_2.txt
557 lines changed

# local install temp_mw_2.txt
cp temp_mw_2.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok  No problems noticed
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91

# push csl-orig to github
cd /c/xampp/htdocs/cologne/csl-orig
git add .
git commit -m "MW: See changes_abbrev.txt at
Ref https://github.com/sanskrit-lexicon/csl-corrections/issues/91"
git push
cd /c/xampp/htdocs/cologne/csl-corrections/app/correction_response/issue91


sync csl-orig at Cologne.
regenerate mw displays at Cologne.

sync this repo.
--------------------------------------------------------
--------------------------------------------------------
--------------------------------------------------------

python parse_corrections1.py temp_cfr_1_scott_double.txt corrections_scott_double.txt temp_mw_1.txt temp_mw_1_work.txt
580 lines read from temp_cfr_1_scott_double.txt
4060 lines written to corrections_double.txt
877277 lines read from temp_mw_1.txt
877277 lines written to temp_mw_1_work.txt


--------------------------------------------------------
python parse_corrections.py temp_cfr_1_scott_misc1.txt corrections_misc1.txt

1 PUI, 2 AP90, 6 SHS

edit corrections_misc1.txt and make corrections to:
- pui.txt
- ap90.txt
- shs.txt



