
readme.txt for csl-corrections/batch_20250418/dictionaries/mw/part3


Based on 
 Category-B.dhaval.remarks.txt
 Category-B.dhaval.remarks.AB.txt
   This has cumulative comments
    I added my comment

Dhaval added his remarks on these in comments starting at
https://github.com/sanskrit-lexicon/csl-corrections/issues/101#issuecomment-3704313629


cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw/part3

cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt
cp temp_mw_0.txt temp_mw_1.txt

  Make changes in temp_mw_1.txt
  simultaneously edit  Category-B.dhaval.remarks.AB.txt

When this editing is done, continue with installation details
---------------------------------------------
  
# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw/part3
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw/part3

----------------------
python diff_to_changes_dict.py temp_mw_0.txt temp_mw_1.txt change_mw.txt
3 changes written to change_mw.txt

grep '**pc:' Category-B.dhaval.remarks.AB.txt > mw_printchange.txt

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw/part3
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250418, mw/part3
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push

------------------------

# csl-corrections

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250418, mw/part3
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw/part3


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

