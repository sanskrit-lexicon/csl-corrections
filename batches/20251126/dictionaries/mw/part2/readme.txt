
readme.txt for csl-corrections/batches/20251126/dictionaries/mw/part2/
Installation of Andhrabharati changes
  Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102#issuecomment-3631988438
  
  AB's response, copied and renamed 
  Category-A.AB.response.txt
  
 This file edited with Jim's comments
 For Emacs org-mode convenience, make this change:
   '**AB comment' => '** AB comment'
   

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw/part2/

cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt
cp temp_mw_0.txt temp_mw_1.txt

  Make changes in temp_mw_1.txt
  simultaneously edit  AB's file

When this editing is done, continue with installation details
---------------------------------------------
  
# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw/part2/
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw/part2/

----------------------
diff temp_mw_0.txt temp_mw_1.txt > diff_mw_0_1.txt

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw/part2/
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20251126, mw/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push

------------------------

# csl-corrections

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20251126, mw/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/mw/part2/


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

