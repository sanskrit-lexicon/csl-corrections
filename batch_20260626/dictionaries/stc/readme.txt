readme.txt for csl-corrections/batch_20260626/dictionaries/stc

STC issue 2821: "s. v." abbreviation split across physical lines.
Ref: https://github.com/sanskrit-lexicon/csl-orig/issues/2821

Workflow followed:

1. Snapshot source:
   cp csl-orig/v02/stc/stc.txt temp_stc_0.txt

2. Apply exact updateByLine changes:
   python csl-orig/v02/stc/abbrev/updateByLine.py temp_stc_0.txt change_stc_1.txt temp_stc_1.txt

   Result:
   164411 lines read from temp_stc_0.txt
   164407 records written to temp_stc_1.txt
   8 change transactions from change_stc_1.txt
   4 of type new, 4 of type del

3. Copy result to csl-orig/v02/stc/stc.txt.

4. Validation:
   cd csl-pywork/v02
   bash generate_dict.sh stc tempparent/stc

   Result:
   make_xml.py: All records parsed by ET

   Local Windows caveats: xmllint and zip were not available; ElementTree parse
   success is the accepted local validation signal per the org AGENTS.md.

5. BOM check:
   first three bytes of csl-orig/v02/stc/stc.txt = 6f2a0a (no UTF-8 BOM).

Note:
This edit deletes four physical line breaks, so the same-line-count
diff_to_changes_dict.py helper is not applicable. The insertion/deletion-aware
diff_to_changes.py helper was not present in the local csl-corrections checkout;
therefore change_stc_1.txt is the exact updateByLine audit file used to apply
the correction.
