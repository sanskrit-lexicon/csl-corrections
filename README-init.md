## Initialization of csl-corrections repository

In broad terms, this repository combines 
* PHP code, currently on Cologne server, for accepting and recording user
  submitted corrections  (in the /php directory at Cologne)
* sanskrit-lexicon/CORRECTIONS repository, whose original purpose was
  to process the user submitted corrections.

Over time, the CORRECTIONS has accumulated additional materials, such as:
* sanhw1 and sanhw2 derived lists of headwords
* various materials related to research studies related to the Cologne
  dictionaries.

## Materials copied from the CORRECTIONS repository
This new csl-corrections repository does NOT include those additional
materials in the CORRECTIONS repository. It does include:
* history.txt  A chronology of processed corrections
* cfr.tsv  The file which records user-submitted corrections
  * 'cfr' stands for 'correction-form-response'
* correctionform.txt a reformattng of cfr.tsv (file generated by cfr_adj.py)
* dictionaries directory containing one subdirectory for each dictionary;
  the name of the directory is the Cologne code for the dictionary.
  The subdirectory for dictionary xxx typically has 2 files:
  * xxx_correctionform.txt  (file generated by cfr_adj.py )
  * xxx_printchange.txt  Manually maintained file, intended to provide
    a history of changes which make the Cologne digitization differ from
    the scanned images (the printed text) of the dictionary. Only a small
    fraction of the corrections are in this category.
* cfr_adj.py  Program which reformats cfr.tsv and produces:
  * correctionform.txt
  * dictionaries/xxx/xxx_correctionform.txt  for all dictionaries xxx 

Note: The following dictionaries xxx have material in dictionaries/xxx in
  addition to xxx_correctionform.txt  and xxx_printchange.txt;
  this additional material remains in the CORRECTIONS repository, but is 
  not currently in the csl-corrections repository.
* acc : faultfinder/
* ae  : issue-306/
* ben : issue-287prep/
* bhs : verbs/
* bur : iastwork/ , issue-296prep/ , verbs/
* cae : issue-275prep/ , issue-289prep/ , issue-290prep/
* ccs : issue-261/ , issue-264/ , issue-265prep/
* ieg : faultfinder/ , foreignwords/
* inm : faultfinder/ , missing_0001-0099.txt
* mci : faultfinder/
* mw  : Hxa/ , issue-298-preverb1/
* mw72: arabicByLine.txt , missing_arabic/ , MW72_history.txt
* mwe : missing/
* pd  : faultfinder/ , issue-108/
* pe  : faultfinder/ , issue-253/
* pgn : pgn-fuzzyalpha.html , pgn-fuzzyalpha.txt
* pui : issue-251/ , pui-fuzzyalpha.html , pui-fuzzyalpha.txt
* pw  : missing_0001-0099.txt
* pwg : ahlborn.txt , missing/ , removenv_all.txt
* skd : alphaerr/ , alphaerrByLine.txt , issue-291prep/ , SKD_history.txt
* vcp : alphaerr/ , VCP_history.txt
* vei : missing/ , vei-fuzzyalpha.txt , vei-fuzzyalpha-completed.txt
* wil : chksort2.txt , factual_corrections.txt
* yat : corrections_factual.txt

## materials copied from Cologne server /php directory
These are copied into a new 'app' directory of csl-corrections
* all correction_form*.php and correction_form*.css files.
  The main application entry point is app/correction_form.php
* the correction_response directory.  This contains:
  * cfr.tsv  Cumulative user-contributed correction form responses
    The first one is dated 03/18/2014.
  * cfr-yyyymmdd.tsv  individual daily correction form responses.
    Since these are duplicated in cfr.tsv, the .gitignore for the
    repository does not track them.  
  * Three .zip files, containing snap-shots of cfr.tsv made in 2015, 2016, 2018.
    Since git is now tracking everything, .gitignore has been modified
    to ignore these.
