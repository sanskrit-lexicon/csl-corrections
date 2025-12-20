
2025-12-18
readme.txt for csl-corrections/batch_20250418/dictionaries/shs

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/shs

python prepedit.py shs_correctionform.txt tempwork_shs_correctionform.txt
223 sections

cp /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt temp_shs_0.txt

cp temp_shs_0.txt temp_shs_1.txt
  Make changes in temp_shs_1.txt
  simultaneously edit  tempwork_shs_correctionform.txt
  Note: change in make_xml.py ('12-19-2025') of csl-pywork


# remake xml from temp_shs_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/shs
cp temp_shs_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh shs  ../../shs
sh xmlchk_xampp.sh shs
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/shs

----------------------
python diff_to_changes_dict.py temp_shs_0.txt temp_shs_1.txt change_shs_1.txt
1660 changes written to change_shs_1.txt
----------------------
# shs_correctionform_edit.txt is tracked by git
cp tempwork_shs_correctionform.txt shs_correctionform_edit.txt

# extract the 'global changes' sections at top of shs_correctionform_edit.txt
# put into readme_shs_global.txt

# extract the print changes
grep '** pc:' shs_correctionform_edit.txt > shs_printchange.txt
wc -l shs_printchange.txt
18 shs_printchange.txt

-------------------------------------------------
# partition shs_correctionform_edit.txt into subgroups,
 for possible further analysis

# shs_done.txt
python separate.py '* TODOx' shs_correctionform_edit.txt shs_done.txt temptodo.txt
222 sections
214 sections written to shs_done.txt
8 sections written to temptodo.txt

# the 8 (not done) are not further classified
mv temptodo.txt shs_todo_misc.txt

----------
Manually Add doc section to the subgroup files

change 'status = PENDING' to 'status = DONE' in shs_done.txt
change 'TODOx ' to ''
================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/shs
diff temp_shs_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250418, shs
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
# return home
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/shs

------------------------

# csl-corrections
# update csl-corrections/dictionaries/shs/shs_printchange.txt from
#  shs_printchange.txt

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250418, shs
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/shs

------------------------

# csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork
git pull
git add .
git commit -m "Scott backlog of 20250418, shs
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/shs

  
---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull
csl-pywork # pull
---------------
# update displays for shs
cd csl-pywork/v02
sh generate_dict.sh shs  ../../SHSScan/2020/

-----------------------------------------------------
THE END
-----------------------------------------------------

