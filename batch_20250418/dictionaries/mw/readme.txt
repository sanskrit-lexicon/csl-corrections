
readme.txt for csl-corrections/batch_20250418/dictionaries/mw

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw

cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt

cp mw_correciontform.txt tempwork_mw_correciontform.txt 

cp temp_mw_0.txt temp_mw_1.txt
  Make changes in temp_mw_1.txt
  simultaneously edit  tempwork_mw_correciontform.txt
  
# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw

----------------------
python diff_to_changes_dict.py temp_mw_0.txt temp_mw_1.txt change_mw_1.txt
236 changes written to change_mw_1.txt
----------------------

Divide the edited tempwork_mw_correciontform.txt into
mw_correctionform_done.txt  (164 cases)
mw_correctionform_todo.txt  (26 cases)

mw_printchange.txt  are the 36 '* pc: ' lines of mw_correctionform_done.txt.

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250418, mw
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push

------------------------

# csl-corrections


cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250418, mw
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw


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
