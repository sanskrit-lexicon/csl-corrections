#echo "This script needs to be run with GitBash on windows OS"
#echo "download new cfr.tsv from Cologne"
#curl -o cfr.tsv https://www.sanskrit-lexicon.uni-koeln.de/php/correction_response/cfr.tsv
echo "regenerate correctionform.txt and dictionaries/xxx/xxx_correctionform.txt"
python3 cfr_adj.py app/correction_response/cfr.tsv correctionform.txt
echo "redo_cfr.sh is finished"
echo "Upload to github issues on sanskrit-lexicon/csl-orig"
python upload_github_issue.py app/correction_response/cfr.tsv

