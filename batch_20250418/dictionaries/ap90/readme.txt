
2025-12-18
readme.txt for csl-corrections/batch_20250418/dictionaries/ap90

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap90

# cp /ap90_correctionform.txt tempwork_ap90_correctionform.txt 
python prepedit.py ap90_correctionform.txt tempwork_ap90_correctionform.txt
# 43 sections

cp /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt temp_ap90_0.txt

cp temp_ap90_0.txt temp_ap90_1.txt
  Make changes in temp_ap90_1.txt
  simultaneously edit  tempwork_ap90_correctionform.txt
  
# remake xml from temp_ap90_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap90
cp temp_ap90_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap90

----------------------
python diff_to_changes_dict.py temp_ap90_0.txt temp_ap90_1.txt change_ap90_1.txt
120 changes written to change_ap90_1.txt

----------------------
# ap90_correctionform_edit.txt is tracked by git
cp tempwork_ap90_correctionform.txt ap90_correctionform_edit.txt
# extract the 'global changes' sections at top of ap90_correctionform_edit.txt
# put into readme_ap90_global.txt

# extract the print changes
grep '** pc:' ap90_correctionform_edit.txt > ap90_printchange.txt
wc -l ap90_printchange.txt
2 ap90_printchange.txt

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap90
diff temp_ap90_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250418, ap90
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/ap90/ap90_printchange.txt from
#  ap90_printchange.txt

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250418, ap90
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/ap90

---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull

---------------
# update displays for ap90
cd csl-pywork/v02
sh generate_dict.sh ap90  ../../AP90Scan/2020/

-----------------------------------------------------
THE END
-----------------------------------------------------

