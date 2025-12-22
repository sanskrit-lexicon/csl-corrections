
2025-12-20
readme.txt for csl-corrections/batches/20251126/dictionaries/shs

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/shs

# cp shs_correctionform.txt tempwork_shs_correctionform.txt 
python prepedit.py shs_correctionform.txt tempwork_shs_correctionform.txt
# 224 cases

cp /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt temp_shs_0.txt

cp temp_shs_0.txt temp_shs_1.txt
  Make changes in temp_shs_1.txt
  simultaneously edit  tempwork_shs_correctionform.txt
  
# remake xml from temp_shs_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/shs
cp temp_shs_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh shs  ../../shs
sh xmlchk_xampp.sh shs
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/shs

*********************************************
Handling of end-of-hyphens in display

Modified csl-pywork: make_xml.py
This solves the problem, by addimg <lb/> to each line

----------------------
python diff_to_changes_dict.py temp_shs_0.txt temp_shs_1.txt change_shs_1.txt
527 changes written to change_shs_1.txt
----------------------
# shs_correctionform_edit.txt is tracked by git
cp tempwork_shs_correctionform.txt shs_correctionform_edit.txt
# extract the 'global changes' sections at top of shs_correctionform_edit.txt
# put into readme_shs_global.txt

# extract the print changes
grep '** pc:' shs_correctionform_edit.txt > shs_printchange.txt
wc -l shs_printchange.txt
44 shs_printchange.txt

-------------------------------------------------
# partition shs_correctionform_edit.txt into subgroups,
 for possible further analysis

# shs_done.txt
python separate.py '* TODOx' shs_correctionform_edit.txt shs_done.txt temptodo.txt
223 sections
220 sections written to shs_done.txt
3 sections written to temptodo.txt

mv temptodo.txt shs_todo_misc.txt


----- subgroup summary
220 shs_done.txt 
  3 shs_toto_misc.txt

----------
Manually Add doc section to the subgroup files

================================================
INSTALLATION
sync to github:

------------------
# csl-orig 
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/shs
diff temp_shs_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20251126, shs
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push

------------------
# csl-orig (1 more correction)
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/shs
diff temp_shs_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20251126, shs
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/shs/shs_printchange.txt from
#  shs_printchange.txt

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20251126, shs
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/shs

------------------------

# csl-pywork
cd /c/xampp/htdocs/cologne/csl-pywork
git pull
git add .
git commit -m "Scott backlog of 20251126, shs end of line hyphenation joining
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/shs

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

