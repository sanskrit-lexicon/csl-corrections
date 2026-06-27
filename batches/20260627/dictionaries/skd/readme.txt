SKD corrections for GitHub issue #13.

Source issue:
https://github.com/sanskrit-lexicon/SKD/issues/13

Scope:
Line-preserving corrections for mismatched square/round brackets and bracket
spillover text in csl-orig/v02/skd/skd.txt.

Validation:
- Applied with updateByLine.py against temp_skd_0.txt snapshot.
- Generated csl-corrections audit file with diff_to_changes_dict.py.
- Confirmed csl-orig/v02/skd/skd.txt has no UTF-8 BOM.
- Confirmed target bad-pattern scan returns no matches.
- Rendered temporary SKD pywork and ran:
  python hw.py ..\orig\skd.txt hwextra\skd_hwextra.txt skdhw.txt
  python make_xml.py ..\orig\skd.txt skdhw.txt skd.xml
- XML parse output included: All records parsed by ET
