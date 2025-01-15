------------------------------------------------------------------------
cp mw.txt /c/xampp/htdocs/cologne/csl-orig/v02/mw/mw.txt
cd /c/xampp/htdocs/cologne/csl-pywork/v02
sh generate_dict.sh mw  ../../mw
sh xmlchk_xampp.sh mw
cd /c/xampp/htdocs/cologne/csl-orig/v02/
git add mw/mw.txt
# make a new issue in csl-orig and note its issue-number
git commit -m "MW:  
 Ref: https://github.com/sanskrit-lexicon/csl-orig/issues/1643#issuecomment-2171829518"
 
git push
# do the necessary for cologne server
# sh generate_dict.sh mw  ../../MWScan/2020/
cd /c/xampp/htdocs/cologne/csl-corrections/temp_batch

cc39ac1ea1f27a9f1e452092f0c882a7e9cba606
For update of csl-corrections
cd /c/xampp/htdocs/cologne/csl-corrections
git commit -m "MW: #1643 mw_todo_misc1.txt
> Ref: https://github.com/sanskrit-lexicon/csl-orig/issues/1643"
