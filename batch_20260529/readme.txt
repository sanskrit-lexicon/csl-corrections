readme.txt for csl-corrections/batch_20260529
Markup whitespace fixes — 2026-05-29

This batch documents automated markup fixes applied to 10 dictionaries in csl-orig.
All fixes were whitespace-only changes inside XML element content (not structural).

## Source

The fixes originated from markup-fix-audit branches in each dict repo (branch
markup-fix-audit in BOR, AP90, GRA, MWS, AP, BUR, INM, KRM, BOP, MW72).
Each branch contained:
  08_markup_fix.py       — script detecting whitespace issues
  markup_fix_changes.txt — updateByLine-format change file
  markup_audit.txt       — full audit of issues found

## Workflow followed (Jim Funderburk pattern)

For each dict:
  1. cp csl-orig/v02/{dict}/{dict}.txt temp_{dict}_0.txt
  2. Apply markup_fix_changes.txt via updateByLine.py
  3. cp temp_{dict}_1.txt csl-orig/v02/{dict}/{dict}.txt
  4. sh generate_dict.sh {dict} tempparent/{dict}  (XML validation)
  5. python diff_to_changes_dict.py temp_{dict}_0.txt temp_{dict}_1.txt change_{dict}_markup_1.txt
  6. Commit csl-orig + csl-corrections

## XML Validation results (generate_dict.sh / make_xml.py)

  BOR    ✅  All records parsed by ET (21990 lines changed)
  AP90   ⚠️  Pre-existing hw.py <LEND> error in intro section (unrelated to our 1 change)
  GRA    ✅  All records parsed by ET (60 lines changed)
  MW     ⚠️  Pre-existing hw.py <LEND> error at lines 3/6/9 (unrelated to our 9 changes)
  AP     ✅  All records parsed by ET (1 line changed)
  BUR    ⚠️  Pre-existing hw.py <LEND> error in intro section (unrelated to our 1 change)
  INM    ✅  All records parsed by ET (1 line changed)
  KRM    ✅  All records parsed by ET (5 lines changed)
  BOP    ✅  All records parsed by ET (39 lines changed)
  MW72   ✅  All records parsed by ET (24 lines changed)

Note: The hw.py <LEND> errors in AP90, MW, BUR are pre-existing and exist in git history
before our commits. xmllint was not available locally; Jim's XAMPP setup would run it.
All structural XML checks passed via Python ElementTree (make_xml.py) where hw.py ran.

## BOM issue found and fixed

Six dicts (ap90, mw, ap, bur, inm, krm) had a spurious UTF-8 BOM added accidentally
when applying the markup fix. This was detected via diff_to_changes_dict.py and fixed
in a separate commit (922602c) before the change files were finalised.
The change files in this batch reflect the correct net diff (no BOM change).

## csl-orig commit references

  BOR:          442e0d7  ai-wip: BOR markup fix
  AP90:         863d559  ai-wip: AP90 markup fix
  GRA:          a74c199  ai-wip: GRA markup fix
  MWS (mw):     8b051ab  ai-wip: MWS markup fix
  AP:           51a764b  ai-wip: AP markup fix
  BUR/INM/KRM:  969e0b8  ai-wip: BUR/INM/KRM markup fixes
  BOP/MW72:     3f53192  ai-wip: BOP/MW72 markup fixes
  BOM removal:  922602c  fix: remove spurious UTF-8 BOM from ap90/mw/ap/bur/inm/krm

## Dictionaries processed

  dictionaries/bor/   change_bor_markup_1.txt    21990 changes  (spaces before </div>)
  dictionaries/ap90/  change_ap90_markup_1.txt   1 change       (trailing space in <ls>)
  dictionaries/gra/   change_gra_markup_1.txt    60 changes     (leading spaces in <chg>)
  dictionaries/mw/    change_mw_markup_1.txt     9 changes      (trailing spaces in <lex><bio><arab><bot><chg><old>)
  dictionaries/ap/    change_ap_markup_1.txt     1 change       (trailing space in <ls>)
  dictionaries/bur/   change_bur_markup_1.txt    1 change       (leading space in <lang n="greek">)
  dictionaries/inm/   change_inm_markup_1.txt    1 change       (trailing space in <is>)
  dictionaries/krm/   change_krm_markup_1.txt    5 changes      (trailing spaces in <s> tags)
  dictionaries/bop/   change_bop_markup_1.txt    39 changes     (leading spaces in <lang n="Avestan"> and <lang n="greek">)
  dictionaries/mw72/  change_mw72_markup_1.txt   24 changes     (whitespace trims in various paired tags)

## Issue references

  BOR  — https://github.com/sanskrit-lexicon/BOR/issues/4
  AP90 — https://github.com/sanskrit-lexicon/AP90/issues/30
  GRA  — https://github.com/sanskrit-lexicon/GRA/issues/37
  MWS  — https://github.com/sanskrit-lexicon/MWS/issues/194
  AP   — https://github.com/sanskrit-lexicon/AP/issues/29
  BUR  — https://github.com/sanskrit-lexicon/BUR/issues/6
  INM  — https://github.com/sanskrit-lexicon/INM/issues/10
  KRM  — https://github.com/sanskrit-lexicon/KRM/issues/4
  BOP  — https://github.com/sanskrit-lexicon/BOP/issues/8
  MW72 — https://github.com/sanskrit-lexicon/MW72/issues/6
