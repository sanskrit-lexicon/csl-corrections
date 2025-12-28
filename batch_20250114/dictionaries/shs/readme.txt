
2025-12-27
readme.txt for csl-corrections/batch_20250114/dictionaries/shs

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/shs


python prepedit.py shs_correctionform.txt tempwork_shs_correctionform.txt
212 sections written to tempwork_shs_correctionform.txt


cp /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt temp_shs_0.txt

cp temp_shs_0.txt temp_shs_1.txt
  Make changes in temp_shs_1.txt
  simultaneously edit  tempwork_shs_correctionform.txt
  
# remake xml from temp_shs_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/shs
cp temp_shs_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh shs  ../../shs
sh xmlchk_xampp.sh shs
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/shs

----------------------
python diff_to_changes_dict.py temp_shs_0.txt temp_shs_1.txt change_shs_1.txt
1237 changes written to change_shs_1.txt
----------------------
# shs_correctionform_edit.txt is tracked by git
cp tempwork_shs_correctionform.txt shs_correctionform_edit.txt

readme_global_shs.txt has global changes made 
63 global chanes.

# extract the print changes
grep '** pc:' shs_correctionform_edit.txt > shs_printchange.txt
wc -l  shs_printchange.txt
32 print changes

-------------------------------------------------
# partition shs_correctionform_edit.txt

# Nothing to do here - There are labels in shs_correctionform_edit.txt
# python separate.py '* TODOx' shs_correctionform_edit.txt shs_done.txt shs_todo.txt

# Manually Add doc section to the subgroup files

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/shs
diff temp_shs_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250114, shs
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/shs/shs_printchange.txt from
#  shs_printchange.txt

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250114, shs
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/shs

---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull

---------------
# update displays for shs
cd csl-pywork/v02
sh generate_dict.sh shs  ../../SHSScan/2020/

-----------------------------------------------------
THE END
-----------------------------------------------------

