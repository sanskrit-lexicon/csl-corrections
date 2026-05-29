readme.txt for csl-corrections/batch_20260529/dictionaries/bur

BUR markup fix — 2026-05-29

Description: Remove leading space inside <lang n="greek"> at line 68267
Changes applied: 1
csl-orig commit: 969e0b8
Issue: https://github.com/sanskrit-lexicon/BUR/issues/6

Workflow:
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/bur
  cp C:/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt temp_bur_0.txt
  # Apply markup_fix_changes.txt (from markup-fix-audit branch)
  python updateByLine.py temp_bur_0.txt ../../../bur/markup-fix-audit/markup_fix_changes.txt temp_bur_1.txt
  cp temp_bur_1.txt C:/xampp/htdocs/cologne/csl-orig/v02/bur/bur.txt

  # Validate XML
  cd C:/xampp/htdocs/cologne/csl-pywork/v02
  sh generate_dict.sh bur  ../../bur
  sh xmlchk_xampp.sh bur
  # XML result: Pre-existing hw.py <LEND> error in intro section (unrelated to this fix)

  # Generate audit trail
  cd C:/xampp/htdocs/cologne/csl-corrections/batch_20260529/dictionaries/bur
  python diff_to_changes_dict.py temp_bur_0.txt temp_bur_1.txt change_bur_markup_1.txt
  # 1 changes written to change_bur_markup_1.txt

Note: A spurious UTF-8 BOM was added by the fix and removed in commit 922602c.

Files:
  change_bur_markup_1.txt  — updateByLine audit trail (1 changes)
