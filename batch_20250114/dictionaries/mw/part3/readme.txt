
2025-12-29
readme.txt for csl-corrections/batch_20250114/dictionaries/mw/part3

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part3


cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt
cp temp_mw_0.txt temp_mw_1.txt

  Make changes in temp_mw_1.txt
  simultaneously edit AB's file
03_TODOP.Placement.AB.txt (AB's posts with Jim's comments)
Also revisions to part2/
01_TODOE.Emergency.AB.txt
02_mw_printchange.AB.txt

Jim's task is to implement the changes posted by Andhrabharati.


# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part3
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part3

-------------------------
diff temp_mw_0.txt temp_mw_1.txt > diff_mw_0_1.txt

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part3
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250114, mw/part3 and revised mw/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part3

------------------------

# csl-corrections
# update csl-corrections/dictionaries/mw/mw_printchange.txt
cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250114, mw/part3 and revised mw/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part3

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

