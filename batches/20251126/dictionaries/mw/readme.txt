
readme.txt for csl-corrections/batches/20251126/dictionaries/mw

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw

cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt

cp mw_correctionform.txt tempwork_mw_correctionform.txt 
# the tempwork file is not tracked by Git, due to the .gitignore of this repo

cp temp_mw_0.txt temp_mw_1.txt
  Make changes in temp_mw_1.txt
  simultaneously edit  tempwork_mw_correctionform.txt
  Continue until done with this analysis

# So git can track
cp tempwork_mw_correctionform.txt mw_correctionform_edit.txt

------------------------------
# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw

----------------------
python diff_to_changes_dict.py temp_mw_0.txt temp_mw_1.txt change_mw_1.txt
144 changes written to change_mw_1.txt
----------------------

# separate mw_correctionform_edit.txt
  into mw_done.txt
  and temptodo.txt
python separate.py '* TODOx' tempwork_mw_correctionform.txt mw_done.txt temptodo.txt
2275 lines read from tempwork_mw_correctionform.txt
skipping first section, whose first line is
Sanskrit Lexicon Correction Form History for MW
316 sections
164 sections written to mw_done.txt
152 sections written to temptodo.txt

# separate temptodo.txt into
  mw_todo_hyphen.txt  ('* TODO-')
  mw_todo_misc.txt ('* TODO ')
python separate.py '* TODO-' temptodo.txt mw_todo_hyphen.txt mw_todo_misc.txt
1108 lines read from temptodo.txt
152 sections
114 sections written to mw_todo_hyphen.txt
38 sections written to mw_todo_misc.txt

---------------
Count the printchanges.  These are lines starting with '** pc:'
grep '** pc:' mw_done.txt | wc -l
38
grep '** pc:' mw_done.txt  > mw_printchange.txt

mw_printchange.txt  are the 36 '* pc: ' lines of mw_correctionform_done.txt.

--------------
manual changes:
1. change 'PENDING' to 'DONE' in mw_done.txt
2. compose 'doc' lines in each of
   mw_done.txt
   mw_todo_hyphen.txt
   mw_todo_misc.txt

------------------------------------------------
add mw_printchange.txt to
 /c/xampp/htdocs/cologne/csl-corrections/dictionaries/mw
 
================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20251126, mw
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push

------------------------

# csl-corrections

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20251126, initialization and mw
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw


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
