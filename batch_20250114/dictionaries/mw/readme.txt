
2025-12-22
readme.txt for csl-corrections/batch_20250114/dictionaries/mw

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw

# 
python prepedit.py mw_correctionform.txt tempwork_mw_correctionform.txt

cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt

cp temp_mw_0.txt temp_mw_1.txt
  Make changes in temp_mw_1.txt
  simultaneously edit  tempwork_mw_correctionform.txt
  
# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw

----------------------
python diff_to_changes_dict.py temp_mw_0.txt temp_mw_1.txt change_mw_1.txt
625 changes written to change_mw_1.txt
----------------------
# mw_correctionform_edit.txt is tracked by git
cp tempwork_mw_correctionform.txt mw_correctionform_edit.txt

readme_mw_global.txt has global changes made 

# extract the print changes
grep '** pc:' mw_correctionform_edit.txt > mw_printchange.txt

15 print changes

-------------------------------------------------
# partition mw_correctionform_edit.txt into 2 subgroups,

# mw_done.txt and mw_todo.txt
python separate.py '* TODOx' mw_correctionform_edit.txt mw_done.txt mw_todo.txt
263 sections written to mw_done.txt
204 sections written to mw_todo.txt


----------
Manually Add doc section to the subgroup files

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250114, mw
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/mw/mw_printchange.txt from
#  mw_printchange.txt

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250114, mw
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw

---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull

---------------
# update displays for mw
cd csl-pywork/v02
sh generate_dict.sh mw  ../../MWScan/2020/

-----------------------------------------------------
THE END
-----------------------------------------------------

