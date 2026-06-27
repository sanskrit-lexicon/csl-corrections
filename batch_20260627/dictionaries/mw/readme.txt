MW correction batch 2026-06-27

Issue:
- sanskrit-lexicon/csl-orig#1537

Source:
- csl-orig/v02/mw/mw.txt

Correction:
- L=179760, source line 599645
- Changed the proper-name citation inside <s> from ruci-ruce to Ruci-ruce.

Files:
- change_mw_1.txt records the paired updateByLine.py old/new correction.

Application and validation:
- Applied with csl-pywork/v02/makotemplates/pywork/updateByLine.py.
- Generated MW with csl-pywork/v02/generate_dict.sh mw tempparent/mw under Git Bash.
- Local XML signal passed: make_xml.py reported "All records parsed by ET".
- Later local steps reported unavailable xmllint/php/zip tooling; these are outside the accepted ET parse gate on this Windows setup.
- UTF-8 BOM check for csl-orig/v02/mw/mw.txt: first three bytes = 3c4c3e.
