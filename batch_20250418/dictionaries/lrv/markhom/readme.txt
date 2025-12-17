
2025-12-16
readme.txt for csl-corrections/batch_20250418/dictionaries/lrv/markhom

Add <h> field to metalines for lrv where appropriate.

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/lrv/markhom

cp /c/xampp/htdocs/cologne/csl-orig/v02/lrv/lrv.txt temp_lrv_0.txt

python markhom.py temp_lrv_0.txt temp_lrv_1.txt
8063 lines changed
Note: There are 8067 metalines with <h>
      4 previously marked

# remake xml from temp_lrv_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/lrv/markhom
cp temp_lrv_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/lrv/lrv.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh lrv  ../../lrv
sh xmlchk_xampp.sh lrv
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/lrv/markhom

----------------------
python ../diff_to_changes_dict.py temp_lrv_0.txt temp_lrv_1.txt change_lrv_1.txt
1666 changes written to change_lrv_1.txt
----------------------

------------------------------------------------
Changes are made to display modules (simple-search, webtc1)
so the list-view will show the homonym.

repos changed: csl-apidev, csl-pywork, csl-websanlexicon

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/lrv/markhom
diff temp_lrv_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/lrv/lrv.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250418, lrv homonyms
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push

------------------------
cd /c/xampp/htdocs/cologne/csl-apidev
git pull
git add .
git commit -m "lrv homonym display in hierarchy
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/lrv/markhom

------------------------
cd /c/xampp/htdocs/cologne/csl-pywork
git pull
git add .
git commit -m "lrv homonym display in hierarchy
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/lrv/markhom
------------------------
cd /c/xampp/htdocs/cologne/csl-websanlexicon
git pull
git add .
git commit -m "lrv homonym display in hierarchy
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/lrv/markhom

------------------------

# csl-corrections

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250418, lrv/part2 homonyms
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/lrv/markhom

---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
# pull these repos
csl-orig 
csl-pywork
csl-websanlexicon
csl-apidev
csl-corrections 

---------------
# update displays for lrv
cd csl-pywork/v02
sh generate_dict.sh lrv  ../../LRVScan/2022/

# also, displays for pwg, pw, pwkvn, sch, md, mw
sh generate_dict.sh pwg  ../../PWGScan/2020/
sh generate_dict.sh pw  ../../PWScan/2020/
sh generate_dict.sh pwkvn  ../../PWKVNScan/2020/
sh generate_dict.sh sch  ../../SCHScan/2020/
sh generate_dict.sh md  ../../MDScan/2020/
sh generate_dict.sh mw  ../../MWScan/2020/
-----------------------------------------------------
THE END
-----------------------------------------------------

