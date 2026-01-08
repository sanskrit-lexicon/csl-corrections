01-07-2026 @funderburkjim

readme.txt for csl-corrections/batches/20251126/dictionaries/mw/part3/

see https://github.com/sanskrit-lexicon/csl-corrections/issues/111

Installation of Andhrabharati changes
https://github.com/sanskrit-lexicon/csl-corrections/issues/102#issuecomment-3705373030
  has link to AB's file.
  20251126.mw_todo_misc.Cat-B.AB.response.txt

 This file edited with Jim's comments
   

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw/part3/

cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt
cp temp_mw_0.txt temp_mw_1.txt

  Make changes in temp_mw_1.txt
  simultaneously edit  AB's file

When this editing is done, continue with installation details
---------------------------------------------
  
# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw/part3/
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw/part3/

----------------------
python diff_to_changes_dict.py temp_mw_0.txt temp_mw_1.txt change_mw_1.txt
3 changes written to change_mw_1.txt

grep 'pc:' 20251126.mw_todo_misc.Cat-B.AB.response.txt > mw_printchange.txt
================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw/part3/
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20251126, mw/part3
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/111"

git push

------------------------

# csl-corrections

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20251126, mw/part3
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/111"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw/part3/


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

