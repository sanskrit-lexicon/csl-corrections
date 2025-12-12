
2025-12-06
readme.txt for csl-corrections/batches/20251126/dictionaries/ap

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap

cp /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt temp_ap_0.txt

# cp ap_correctionform.txt tempwork_ap_correctionform.txt 
python prepedit.py ap_correctionform.txt tempwork_ap_correctionform.txt

cp temp_ap_0.txt temp_ap_1.txt
  Make changes in temp_ap_1.txt
  simultaneously edit  tempwork_ap_correctionform.txt

# revise csl-pywork/v02/makotemplates/pywork/one.dtd to handle '<ns>'

# remake xml from temp_ap_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap
cp temp_ap_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap  ../../ap
sh xmlchk_xampp.sh ap
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap

----------------------
python diff_to_changes_dict.py temp_ap_0.txt temp_ap_1.txt change_ap_1.txt
1675 changes written to change_ap_1.txt
----------------------

# ap_correctionform_edit.txt is tracked by git
cp tempwork_ap_correctionform.txt ap_correctionform_edit.txt

# extract the print changes
grep '** pc:' ap_correctionform_edit.txt > ap_printchange.txt
wc -l ap_printchange.txt
83 ap_printchange.txt

-------------------------------------------------
# partition ap_correctionform_edit.txt into subgroups,
 for possible further analysis

# ap_done.txt
python separate.py '* TODOx' ap_correctionform_edit.txt ap_done.txt temptodo.txt
1612 sections
1478 sections written to ap_done.txt
134 sections written to temptodo.txt

python separate.py '* TODO-' temptodo.txt ap_todo_hyphen.txt temptodo1.txt
134 sections
122 sections written to ap_todo_hyphen.txt
12 sections written to temptodo1.txt

cp temptodo1.txt ap_todo_misc.txt

----- subgroup summary
1478 ap_done.txt #
 122 ap_todo_hyphen.txt #
  12 ap_todo_misc.txt
 (+ 1478 122 12) = 1612 as expected

----------
Manually Add doc section to the subgroup files
 (also change PENDING to DONE in ap_done.txt
 
================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap
diff temp_ap_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20251126, ap
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push

------------------------

# csl-pywork/v02

cd /c/xampp/htdocs/cologne/csl-pywork
git pull
git add .
git commit -m "Scott backlog of 20251126, ap
Revise scope of 'ns' tag.
Example in ap.txt at  L=8138, hw=itkawaH 
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap

------------------------

# csl-corrections
# manually, update csl-corrections/dictionaries/ap/ap_printchange.txt from
#  ap_printchange.txt of this 20251126... directory

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20251126, ap
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap

---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull
csl-pywork # pull

---------------
# update displays for ap
cd csl-pywork/v02
sh generate_dict.sh ap  ../../APScan/2020/

-----------------------------------------------------
THE END
-----------------------------------------------------
2025-11-30  Addtional changes from Andhrabharati
  Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102#issuecomment-3589140044
 See subdirectory part2
 
