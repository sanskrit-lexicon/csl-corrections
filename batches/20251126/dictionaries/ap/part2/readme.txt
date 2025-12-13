
readme.txt for csl-corrections/batches/20251126/dictionaries/ap/part2/
Installation of Andhrabharati changes
  Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102#issuecomment-3647228881
  
  AB's response in file:
  20251126.ap_todo_misc.AB.response.txt
  
 This file edited with Jim's comments
 For Emacs org-mode convenience, make this change:
   '**AB comment' => '** AB comment'
   

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap/part2/

cp /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt temp_ap_0.txt
cp temp_ap_0.txt temp_ap_1.txt

  Make changes in temp_ap_1.txt
  simultaneously edit  AB's file

When this editing is done, continue with installation details
---------------------------------------------
  
# remake xml from temp_ap_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap/part2/
cp temp_ap_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap  ../../ap
sh xmlchk_xampp.sh ap
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap/part2/

----------------------
diff temp_ap_0.txt temp_ap_1.txt > diff_ap_0_1.txt

================================================
A correction to mw
cp /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt temp_mw_0.txt
cp temp_mw_0.txt temp_mw_1.txt

Just these 2 changes
pc: 16159 : arDacandrAkAra : arDacandrAkfta : arDacandrAkfti
pc: 16159.1 : arDacandrAkfta : arDacandrAkfta : arDacandrAkfti : headword change

# remake xml from temp_mw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap/part2/
cp temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap/part2
================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap/part2/
diff temp_ap_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt | wc -l
#0  as expected
diff temp_mw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20251126, ap/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push

------------------------

# csl-corrections

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20251126, ap/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/ap/part2/


---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull

---------------
# update displays for ap, mw
cd csl-pywork/v02
sh generate_dict.sh ap  ../../APScan/2020/
sh generate_dict.sh mw  ../../MWScan/2020/

-----------------------------------------------------
THE END

