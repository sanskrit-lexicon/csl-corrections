
2025-12-29
readme.txt for csl-corrections/batch_20250114/dictionaries/mw/part4

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part4


cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt
cp temp_mw_0.txt temp_mw_1.txt

Make changes in temp_mw_1.txt
simultaneously edit AB's files:
03_TODORS.Revision.Symbol.Missing.AB.txt 
04_TODODS.Double.Supplement.AB.txt  done (no changes)
05_TODOI.Indentation.AB.txt  
06_TODOMHW.Missing.Headword.AB.txt  
07_TODOQ.A.question.from.Scott.AB.txt
08_L_out_of_order.AB.txt  (file made by Jim)

Jim's task is to implement the changes posted by Andhrabharati.


# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part4
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part4

-------------------------
diff temp_mw_0.txt temp_mw_1.txt > diff_mw_0_1.txt

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part4
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250114, mw/part4 and revised mw/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part4

------------------------

# csl-corrections
# update csl-corrections/dictionaries/mw/mw_printchange.txt
cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250114, mw/part4 
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/104"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250114/dictionaries/mw/part4

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

