=== 2026-07 BATCH — SHIPPED 12-07-2026 ===
Batch PR: https://github.com/sanskrit-lexicon/csl-orig/pull/2879 (@WAITING maintainer merge; auto-merge OFF)
Dict: ap90 · 15 line changes (14 + 1) · issues AP90#14 + CORRECTIONS#434
Re-validated against csl-orig origin/main HEAD 8e9d7bc9 at batch time: updateByLine 14/14 + 1/1
  applied cleanly (no relocation needed), line-count parity 273715->273715, make_xml.py
  "All records parsed by ET" (34882 entries) in an isolated build outdir (csl-orig NOT
  modified during validation), BOM clean (3c4c3e). xmllint DTD check not run (xmllint absent).
Workflow: queued via /cologne-correction-queue, shipped via /cologne-batch-pr.
Shipped by: Opus 4.8 (claude-opus-4-8), 12-07-2026.

--- per-change provenance ---

11-07-2026 🔵 change_ap90_1.txt — AP90#14 residual paired-parens-outside-Devanagari (14 instances)  [XML-validated 12-07-2026, see below]
  Issue: https://github.com/sanskrit-lexicon/AP90/issues/14
  Description: {#(X)#} -> ({#X#}) — moves parenthesis pairs outside the SLP1
    Devanagari markup, matching the pattern already applied in the maintainer's
    prior 513-change pass on this issue. These 14 are residual instances that
    pass missed. Superseded PR #2863 (branch fix/ap90-paren-outside-slp1),
    which bundled these lines together with unrelated already-shipped/duplicate
    changes to mw.txt and stc.txt — this queue entry carries ONLY the ap90.txt
    lines, re-located by content against current csl-orig main (line numbers
    shifted since #2863 was opened) and re-verified all 14 unique matches.
  Validated: updateByLine.py applied 14/14 "new" transactions cleanly against
    current v02/ap90/ap90.txt (273715 lines in, 273715 lines out); output BOM
    check clean (first bytes 3c4c3e).
  Validated (🔵, 12-07-2026): make_xml.py XML-parse validation COMPLETED. Built ap90
    in an ISOLATED scratch outdir (generate_dict.sh ap90 <scratch>), then swapped the
    corrected text into <scratch>/orig/ap90.txt and re-ran redo_hw.sh + redo_xml.sh:
    34,882 entries found; make_xml.py reported "All records parsed by ET" — well-formed
    XML, no ParseError. **csl-orig was NEVER modified** (verified clean vs HEAD before
    and after — the earlier swap-into-csl-orig block was avoided entirely by validating
    in the outdir). Structurally sound by construction too: the paren move
    {#(X)#} -> ({#X#}) only relocates plain-text parentheses relative to the <s>
    Devanagari markup, which cannot break XML well-formedness. Caveat: xmllint DTD
    validation not run (xmllint absent locally); the ET-parse is the primary structural
    check, DTD-level checks are a maintainer follow-up if desired.
  Prepared by: Sonnet 5 (claude-sonnet-5), 11-07-2026.
  Validated by: Opus 4.8 (claude-opus-4-8), 12-07-2026.

11-07-2026 🔵 change_ap90_2.txt — CORRECTIONS#434 "AP90 - Compounds stated twice": sarpis (L29859) residual
  Issue: https://github.com/sanskrit-lexicon/CORRECTIONS/issues/434
  Description: Removes the duplicate, unbracketed "--Comp." marker at physical
    line 257097 of the sarpis entry (29859): "of the seven seas. --Comp.
    {#--AsutiH#}" -> "of the seven seas. {#--AsutiH#}". Maintainer SergeA
    verified against ed.3 (1924): all three reported cases (ayAta, muKaM,
    sarpis) are 1st-edition print errors with no duplication in ed.3. The other
    two (ayAta L3946, muKaM L23227) already carry a single {@--Comp.@} in
    current csl-orig — sarpis is the residual instance.
  Validated: updateByLine.py applied 1/1 "new" transaction cleanly against
    current v02/ap90/ap90.txt (273715 lines in, 273715 lines out — line-count
    parity); output BOM check clean (first bytes 3c4c3e); diff is exactly the
    one intended line; all {#..#}/{@..@}/{%..%}/<..>/[..] markup-delimiter
    counts identical old-vs-new (text-only edit, no markup touched); full
    generate_dict.sh XML rebuild against a temp swap-in returned "All records
    parsed by ET" (make_xml.py, exit 0), csl-orig restored byte-identical to
    HEAD afterward.
  Prepared by: Opus 4.8 (claude-opus-4-8), 11-07-2026 (G13, handoff H756).
