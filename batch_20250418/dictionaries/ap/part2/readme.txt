
2025-01-02
readme.txt for csl-corrections/batch_20250418/dictionaries/ap/part2

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap/part2

ap_todo_misc.AB.txt at
 https://github.com/sanskrit-lexicon/csl-corrections/issues/101#issuecomment-37002842552
 
cp /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt temp_ap_0.txt


cp temp_ap_0.txt temp_ap_1.txt
  Make changes in temp_ap_1.txt
  simultaneously edit  ap_todo_misc.AB.txt
  
  
# remake xml from temp_ap_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap/part2
cp temp_ap_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap  ../../ap
sh xmlchk_xampp.sh ap
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap/part2

----------------------
python diff_to_changes_dict.py temp_ap_0.txt temp_ap_1.txt change_ap_1.txt
22 changes written to change_ap_1.txt
----------------------

# extract the print changes
grep '**pc:' ap_todo_misc.AB.txt > ap_printchange.txt
wc -l ap_printchange.txt
16 ap_printchange.txt

# use ap_printchange.txt to revise
# csl-corrections/dictionaries/ap/ap_printchange.txt

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap/part2
diff temp_ap_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap/ap.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250418, ap/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/ap/part2/ap_printchange.txt from
#  ap_printchange.txt

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250418, ap/part2
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap/part2


---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull

---------------
# update displays for ap
cd csl-pywork/v02
sh generate_dict.sh ap  ../../APScan/2020/

-----------------------------------------------------
THE END
