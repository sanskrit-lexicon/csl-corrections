
2025-12-26
readme.txt for csl-corrections/batch_20250114/dictionaries/lrv

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/lrv


python prepedit.py lrv_correctionform.txt tempwork_lrv_correctionform.txt
181 sections written to tempwork_lrv_correctionform.txt


cp /c/xampp/htdocs/cologne/csl-orig/v02/lrv/lrv.txt temp_lrv_0.txt

cp temp_lrv_0.txt temp_lrv_1.txt
  Make changes in temp_lrv_1.txt
  simultaneously edit  tempwork_lrv_correctionform.txt
  
# remake xml from temp_lrv_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/lrv
cp temp_lrv_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/lrv/lrv.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh lrv  ../../lrv
sh xmlchk_xampp.sh lrv
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/lrv

----------------------
python diff_to_changes_dict.py temp_lrv_0.txt temp_lrv_1.txt change_lrv_1.txt
437 changes written to change_lrv_1.txt
----------------------
# lrv_correctionform_edit.txt is tracked by git
cp tempwork_lrv_correctionform.txt lrv_correctionform_edit.txt

readme_global_lrv.txt has global changes made 
34 global chanes.


# extract the print changes
grep '** pc:' lrv_correctionform_edit.txt > lrv_printchange.txt

6 print changes

-------------------------------------------------
# partition lrv_correctionform_edit.txt

# Nothing to do here - There are labels in lrv_correctionform_edit.txt
# python separate.py '* TODOx' lrv_correctionform_edit.txt lrv_done.txt lrv_todo.txt

# Manually Add doc section to the subgroup files

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/lrv
diff temp_lrv_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/lrv/lrv.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250114, lrv
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/lrv/lrv_printchange.txt from
#  lrv_printchange.txt

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250114, lrv
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/lrv

---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull

---------------
# update displays for lrv
cd csl-pywork/v02
sh generate_dict.sh lrv  ../../LRVScan/2020/

-----------------------------------------------------
THE END
-----------------------------------------------------

