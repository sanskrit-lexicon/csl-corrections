
2025-12-01
readme.txt for csl-corrections/batch_20250418/dictionaries/ap

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap

cp /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt temp_ap_0.txt

# cp ap_correctionform.txt tempwork_ap_correctionform.txt 
python prepedit.py ap_correctionform.txt tempwork_ap_correctionform.txt

cp temp_ap_0.txt temp_ap_1.txt
  Make changes in temp_ap_1.txt
  simultaneously edit  tempwork_ap_correctionform.txt
  
# remake xml from temp_ap_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap
cp temp_ap_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap  ../../ap
sh xmlchk_xampp.sh ap
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap

----------------------
python diff_to_changes_dict.py temp_ap_0.txt temp_ap_1.txt change_ap_1.txt
602 changes written to change_ap_1.txt
----------------------
# ap_correctionform_edit.txt is tracked by git
cp tempwork_ap_correctionform.txt ap_correctionform_edit.txt

# extract the print changes
grep '** pc:' ap_correctionform_edit.txt > ap_printchange.txt
wc -l ap_printchange.txt
60 ap_printchange.txt

-------------------------------------------------
# partition ap_correctionform_edit.txt into subgroups,
 for possible further analysis

# ap_done.txt
python separate.py '* TODOx' ap_correctionform_edit.txt ap_done.txt temptodo.txt
603 sections  one extra section 'Case 0' added manually
506 sections written to ap_done.txt
97 sections written to temptodo.txt

python separate.py '* TODO-' temptodo.txt ap_todo_hyphen.txt temptodo1.txt
53 sections written to ap_todo_hyphen.txt
44 sections written to temptodo1.txt

python separate.py '* TODOd' temptodo1.txt ap_todo_display.txt temptodo2.txt
8 sections written to ap_todo_display.txt
36 sections written to temptodo2.txt

python separate.py '* TODOm' temptodo2.txt ap_todo_M_vowel.txt temptodo3.txt
3 sections written to ap_todo_M_vowel.txt
33 sections written to temptodo3.txt

python separate.py '* TODOg1' temptodo3.txt ap_todo_g1.txt temptodo4.txt
3 sections written to ap_todo_g1.txt
30 sections written to temptodo4.txt

python separate.py '* TODOh' temptodo4.txt ap_todo_hwmiss.txt temptodo5.txt
2 sections written to ap_todo_hwmiss.txt
28 sections written to temptodo5.txt

cp temptodo5.txt ap_todo_misc.txt

----- subgroup summary
506 ap_done.txt #
 53 ap_todo_hyphen.txt #
  8 ap_todo_display.txt @
  3 ap_todo_M_vowel.txt @
  3 ap_todo_g1.txt  (€1P. etc.)@
  2 ap_todo_hwmiss.txt@
 28 ap_todo_misc.txt
 (+ 506 53 8 3 3 2 28) = 603 as expected

----------
Manually Add doc section to the subgroup files

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap
diff temp_ap_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250418, ap
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/ap/ap_printchange.txt from
#  ap_printchange.txt

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250418, ap
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap


---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull

---------------
# update displays for ap
cd csl-pywork/v02
sh generate_dict.sh ap  ../../APScan/2020/

-----------------------------------------------------
THE END
-----------------------------------------------------
2025-11-30  Addtional changes from Andhrabharati
  Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101#issuecomment-3589140044
 See subdirectory part2
 
