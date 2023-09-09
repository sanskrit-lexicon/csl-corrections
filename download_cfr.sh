echo "downloading cfr.tsv from Cologne server"
echo "local file is app/correction_response/cfr.tsv"
cd app/correction_response/
curl -o cfr.tsv https://www.sanskrit-lexicon.uni-koeln.de/scans/csl-corrections/app/correction_response/cfr.tsv
echo "Suggest you edit this, go to bottom and remove lines with bad data"
