
2025-12-28
readme.txt for csl-corrections/batch_20250114/dictionaries/mw/part2

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part2


cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt

cp temp_mw_0.txt temp_mw_1.txt
  Make changes in temp_mw_1.txt
  simultaneously edit  mw_todo.txt

Jim's task is to implement the changes posted by Andhrabharati.
The following are AB's posts, with Jim's comments

01_TODOE.Emergency.AB.txt
  Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104#issuecomment-3693804450
02_mw_printchange.AB.txt

# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part2
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part2


================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part2
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250114, mw/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/mw/mw_printchange.txt
cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250114, mw/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part2

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

