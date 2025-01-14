------------------------------------------------------------------------
install mw
cp mw.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
cd /c/xampp/htdocs/cologne/csl-orig/v02/
git add mw/mw.txt
# make a new issue in csl-orig and note its issue-number
git commit -m "MW:  correction backlog, 6.
 Ref: https://github.com/sanskrit-lexicon/csl-orig/issues/1645"
 
git push
# do the necessary for cologne server
# sh generate_dict.sh mw  ../../MWScan/2020/
cd /c/xampp/htdocs/cologne/csl-corrections/temp_batch1

For update of csl-corrections
cd /c/xampp/htdocs/cologne/csl-corrections
git commit -m "MW print changes:  correction backlog, 6. 
 Ref: https://github.com/sanskrit-lexicon/csl-orig/issues/1645"
 

------------------------------------------------------------------------
install ap90
cp ap90.txt /c/xampp/htdocs/cologne/csl-orig/v02/ap90/ap90.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh ap90  ../../ap90
sh xmlchk_xampp.sh ap90
cd /c/xampp/htdocs/cologne/csl-orig/v02/
git add ap90/ap90.txt
# make a new issue in csl-orig and note its issue-number
git commit -m "AP90:  correction backlog, 6.
 Ref: https://github.com/sanskrit-lexicon/csl-orig/issues/1645"
 
git push
# do the necessary for cologne server
# sh generate_dict.sh ap90  ../../AP90Scan/2020/
cd /c/xampp/htdocs/cologne/csl-corrections/temp_batch1

------------------------------------------------------------------------
install shs
cp shs.txt /c/xampp/htdocs/cologne/csl-orig/v02/shs/shs.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh shs  ../../shs
sh xmlchk_xampp.sh shs
cd /c/xampp/htdocs/cologne/csl-orig/v02/
git add shs/shs.txt

git commit -m "SHS: correction backlog, 6.  missed these in last commit
 Ref: https://github.com/sanskrit-lexicon/csl-orig/issues/1645"

git push
# do the necessary for cologne server
# sh generate_dict.sh shs  ../../SHSScan/2020/
cd /c/xampp/htdocs/cologne/csl-corrections/temp_batch1

For update of csl-corrections
cd /c/xampp/htdocs/cologne/csl-corrections
git commit -m "SHS print changes:  correction backlog, 6. 
 Ref: https://github.com/sanskrit-lexicon/csl-orig/issues/1645"

------------------------------------------------------------------------
install pui
cp pui.txt /c/xampp/htdocs/cologne/csl-orig/v02/pui/pui.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh pui  ../../pui
sh xmlchk_xampp.sh pui
cd /c/xampp/htdocs/cologne/csl-orig/v02/
git add pui/pui.txt

git commit -m "PUI:  correction backlog, 6.
 Ref: https://github.com/sanskrit-lexicon/csl-orig/issues/1645"

git push
# do the necessary for cologne server
# sh generate_dict.sh pui  ../../PUIScan/2020/
cd /c/xampp/htdocs/cologne/csl-corrections/temp_batch1
