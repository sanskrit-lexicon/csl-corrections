
2025-12-18
readme.txt for csl-corrections/batch_20250418/dictionaries/pui

cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/pui

pui_correctionform.txt has only 1 item.
 See that file for discussion supporting Scott's print change
edit  /c/xampp/htdocs/cologne/csl-orig/v02/pui/pui.txt

# remake xml  and check
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/pui
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh pui  ../../pui
sh xmlchk_xampp.sh pui
# ok, as expected
# return here
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/pui

================================================
INSTALLATION
sync to github:

------------------
# csl-orig
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/pui
cd /c/xampp/htdocs/cologne/csl-orig/
git pull
git add .
git commit -m "Scott backlog of 20250418, pui
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push

------------------------

# csl-corrections
# update csl-corrections/dictionaries/pui/pui_printchange.txt 

cd /c/xampp/htdocs/cologne/csl-corrections
git pull
git add .
git commit -m "Scott backlog of 20250418, pui
Ref: https://github.com/sanskrit-lexicon/csl-corrections/issues/101"

git push
cd /c/xampp/htdocs/cologne/csl-corrections/batch_20250418/dictionaries/pui

---------------------------------------------------
# sync to Cologne, pull changed repos, redo display
---------------
csl-orig #pull
csl-corrections #pull

---------------
# update displays for pui
cd csl-pywork/v02
sh generate_dict.sh pui  ../../PUIScan/2020/

-----------------------------------------------------
THE END
-----------------------------------------------------

