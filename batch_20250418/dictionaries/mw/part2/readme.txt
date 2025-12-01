
readme.txt for csl-corrections/batch_20250418/dictionaries/mw/part2
Installation of Andhrabharati changes
  Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101#issuecomment-3589140044
  AB's two files:
  Category-A.AB.response.txt
  Category-C.AB.response.txt
 These two files here edited with Jim's comments
 For Emacs org-mode convenience, make these two changes in both AB files:
   '*AB comments' => '** AB comments'
   'TODO CASE' => '* TODO CASE'
  
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw/part2

cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt
cp temp_mw_0.txt temp_mw_1.txt

  Make changes in temp_mw_1.txt
  simultaneously edit  AB's files

When this editing is done, continue with installation details
---------------------------------------------
  
# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw/part2
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw/part2

----------------------
diff temp_mw_0.txt temp_mw_1.txt > diff_mw_0_1.txt

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw/part2
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250418, mw/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push

------------------------

# csl-corrections

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250418, mw/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/mw/part2


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

