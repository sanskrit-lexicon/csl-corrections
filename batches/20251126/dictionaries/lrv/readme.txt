
2025-12-17
readme.txt for csl-corrections/batches/20251126/dictionaries/lrv

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/lrv

# cp lrv_correctionform.txt tempwork_lrv_correctionform.txt 
python prepedit.py lrv_correctionform.txt tempwork_lrv_correctionform.txt
# 179 cases

cp /c/xampp/htdocs/cologne/csl-orig/v02/lrv/lrv.txt temp_lrv_0.txt

cp temp_lrv_0.txt temp_lrv_1.txt
  Make changes in temp_lrv_1.txt
  simultaneously edit  tempwork_lrv_correctionform.txt
  
# remake xml from temp_lrv_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/lrv
cp temp_lrv_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/lrv/lrv.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh lrv  ../../lrv
sh xmlchk_xampp.sh lrv
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/lrv

----------------------
python diff_to_changes_dict.py temp_lrv_0.txt temp_lrv_1.txt change_lrv_1.txt
116 changes written to change_lrv_1.txt
----------------------
# lrv_correctionform_edit.txt is tracked by git
cp tempwork_lrv_correctionform.txt lrv_correctionform_edit.txt
# extract the 'global changes' sections at top of lrv_correctionform_edit.txt
# put into readme_lrv_global.txt

# extract the print changes
grep '** pc:' lrv_correctionform_edit.txt > lrv_printchange.txt
wc -l lrv_printchange.txt
10 lrv_printchange.txt

-------------------------------------------------
# partition lrv_correctionform_edit.txt into subgroups,
 for possible further analysis

# lrv_done.txt
python separate.py '* TODOx' lrv_correctionform_edit.txt lrv_done.txt temptodo.txt
178 sections
113 sections written to lrv_done.txt
65 sections written to temptodo.txt


python separate.py '* TODO-' temptodo.txt lrv_todo_hyphen.txt temptodo1.txt
65 sections
27 sections written to lrv_todo_hyphen.txt
38 sections written to temptodo1.txt


python separate.py '* TODOHOM' temptodo1.txt lrv_done_hom.txt temptodo2.txt
38 sections written to lrv_done_hom.txt
0 sections written to temptodo2.txt


There are no more sections (so, no lrv_todo_misc.txt !)


----- subgroup summary
113 lrv_done.txt #
 27 lrv_todo_hyphen.txt #
 38 lrv_done_hom.txt 
 (+ 113 27 38) = 178 as expected

----------
Manually Add doc section to the subgroup files

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/lrv
diff temp_lrv_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/lrv/lrv.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20251126, lrv
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/lrv/lrv_printchange.txt from
#  lrv_printchange.txt

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20251126, lrv
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/lrv

---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull

---------------
# update displays for lrv
cd csl-pywork/v02
sh generate_dict.sh lrv  ../../LRVScan/2022/

-----------------------------------------------------
THE END
-----------------------------------------------------

