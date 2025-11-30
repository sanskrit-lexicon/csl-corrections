
begin 20251130
readme.txt for csl-corrections/batches/20251126/dictionaries/pw

cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/pw

cp /c/xampp/htdocs/cologne/csl-orig/v02/pw/pw.txt temp_pw_0.txt

cp pw_correctionform.txt tempwork_pw_correctionform.txt 
# the tempwork file is not tracked by Git, due to the .gitignore of this repo

cp temp_pw_0.txt temp_pw_1.txt
  Make changes in temp_pw_1.txt
  simultaneously edit  tempwork_pw_correctionform.txt
  Continue until done with this analysis

# So git can track
cp tempwork_pw_correctionform.txt pw_correctionform_edit.txt

------------------------------
# remake xml from temp_pw_1.txt and check
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/pw
cp temp_pw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/pw/pw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh pw  ../../pw
sh xmlchk_xampp.sh pw
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/pw

----------------------
python diff_to_changes_dict.py temp_pw_0.txt temp_pw_1.txt change_pw_1.txt
12 changes written to change_pw_1.txt

----------------------
print changes
Count the printchanges.  These are lines starting with '** pc:'
grep '** pc:' pw_correctionform_edit.txt | wc -l
1
grep '** pc:' pw_correctionform_edit.txt > pw_printchange.txt

add pw_printchange.txt to
 /c/xampp/htdocs/cologne/csl-corrections/dictionaries/pw
 
================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/pw
diff temp_pw_1.txt /c/xampp/htdocs/cologne/csl-orig/v02/pw/pw.txt | wc -l
#0  as expected
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20251126, pw
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/pw

------------------------
# csl-corrections

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20251126, pw
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/102"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batches/20251126/dictionaries/pw

---------------------------------------------------
# sync to Cologne, pull changed repos, redo display

csl-orig #pull
csl-corrections #pull

---------------
# update displays for pw
cd csl-pywork/v02
sh generate_dict.sh pw  ../../PWScan/2020/

-----------------------------------------------------
THE END
