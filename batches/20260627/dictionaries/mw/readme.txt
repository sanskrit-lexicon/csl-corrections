MW correction for csl-orig GitHub issue #1537.

Source issue:
https://github.com/sanskrit-lexicon/csl-orig/issues/1537

Scope:
Single capitalization correction at L=179760, headword `rocana`:
`ruci-ruce r˚` -> `Ruci-ruce r˚`.

Validation:
- Applied with updateByLine.py against temp_mw_0.txt snapshot.
- Generated csl-corrections audit file with diff_to_changes_dict.py.
- Confirmed csl-orig/v02/mw/mw.txt has no UTF-8 BOM.
- Confirmed the old lower-case pattern is absent and the corrected line is present.
- Rendered temporary MW pywork and ran:
  python hw.py ..\orig\mw.txt hwextra\mw_hwextra.txt mwhw.txt
  python make_xml.py ..\orig\mw.txt mwhw.txt mw.xml
- XML parse output included: All records parsed by ET
