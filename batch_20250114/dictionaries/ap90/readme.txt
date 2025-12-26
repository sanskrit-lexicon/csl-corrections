
2025-12-22
readme.txt for csl-corrections/batch_20250114/dictionaries/ap90

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/ap90

This batch of ap90 changes was previously worked on at
https://github.com/sanskrit-lexicon/ap90/issues/26

I'll gp through it again, maybe a few additional items will be handled.
# 
python prepedit.py ap90_correctionform.txt tempwork_ap90_correctionform.txt
144 sections written to tempwork_ap90_correctionform.txt


cp /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt temp_ap90_0.txt

cp temp_ap90_0.txt temp_ap90_1.txt
  Make changes in temp_ap90_1.txt
  simultaneously edit  tempwork_ap90_correctionform.txt
  
# remake xml from temp_ap90_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/ap90
cp temp_ap90_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/ap90

----------------------
python diff_to_changes_dict.py temp_ap90_0.txt temp_ap90_1.txt change_ap90_1.txt
18 changes written to change_ap90_1.txt
----------------------
# ap90_correctionform_edit.txt is tracked by git
cp tempwork_ap90_correctionform.txt ap90_correctionform_edit.txt

readme_global_ap90.txt has global changes made 

# extract the print changes
grep '** pc:' ap90_correctionform_edit.txt > ap90_printchange.txt

8 print changes

-------------------------------------------------
# partition ap90_correctionform_edit.txt

# Nothing to do here -- all are 'done'
# python separate.py '* TODOx' ap90_correctionform_edit.txt ap90_done.txt ap90_todo.txt

# Manually Add doc section to the subgroup files

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/ap90
diff temp_ap90_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250114, ap90
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/ap90/ap90_printchange.txt from
#  ap90_printchange.txt

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250114, ap90
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/ap90

---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull

---------------
# update displays for ap90
cd csl-pywork/v02
sh generate_dict.sh ap90  ../../AP90Scan/2020/

-----------------------------------------------------
THE END
-----------------------------------------------------

