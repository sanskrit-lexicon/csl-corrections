# BATCH_RUNBOOK.md — metadoc

_Created: 10-07-2026 · Last updated: 11-07-2026_

Companion record for
[docs/BATCH_RUNBOOK.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/BATCH_RUNBOOK.md).

## Purpose & audience

The operator manual for the correction *lifecycle around* the application
workflow: intake (form → daily cron → registry) → preflight → batch assembly →
derived data → issue-taxonomy upkeep. Audience: a new operator/contributor who
must process a correction batch without reading source code. Deliberately does
NOT duplicate the 8-stage application workflow — that stays owned by
[docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md).

## Provenance

Authored 10-07-2026 by Fable 5 (`claude-fable-5`) under
[H502](https://github.com/gasyoun/Uprava/blob/main/handoffs/archive/H502-Fable_csl-corrections_batch_processing_runbook_manual_10.07.26.md)
(the H501–H531 manual-coverage programme; modelled on the
[Litpam-Indexator MANUAL](https://github.com/gasyoun/RussianRamayana/blob/main/Litpam-Indexator/docs/indesign-pipeline/MANUAL.md)
gold standard). Facts read from the tree at commit `60d8e93`: script line
counts, the cron workflow, `cfr_ab.tsv`/`correctionform.txt` shapes, batch
readmes, README-documented counts (39,540 loci rows; 26,246 CFR records).
**One census correction made while writing:** the `*_label/_verify/_project`
scripts turned out to be GitHub issue-taxonomy automation (partly one-shot
backfills with hardcoded issue lists), not correction-content labeling as the
minting census assumed — the manual documents the rerun rules accordingly.

## Known limitations / caveats

- The daily-cron description reflects the workflow file as of 10-07-2026; if
  the Cologne fetch endpoint or schedule changes, §3.0 ages silently.
- The historical intake scripts (§3.5) are described for legibility, not
  re-verified end-to-end (the Google-Form era is closed).
- Script line counts in the appendix drift with every edit — they identify,
  not measure.

## Improvement backlog (ranked)

1. *(open)* A worked end-to-end example: one real (small) issue taken from
   preflight through batch readme to the consolidated PR, with the exact grep
   hits shown.
2. *(open)* Document the Cologne-server side of the intake (form deploy,
   `gitupdate.sh`) once/if server access is ever in scope.
3. *(open)* Fold the `validate_mermaid*.py` diagram checkers into CI so the
   workflow doc's diagrams can't silently break.

## Maintenance rule

Any PR that adds a script, changes the cron, or moves a batch-folder
convention must update the runbook (§1/§3) in the same pass and tick a row
here.

## Intended use / known misuse

**For:** a new operator or contributor running the `csl-corrections` batch
pipeline end to end without reading the scripts — knowing which command to run
at which stage (§1 cheat-sheet), what the registry (`cfr_ab.tsv`,
`correctionform.txt`) means before touching an old issue (§3.2 preflight), how
a batch folder is shaped (§3.3), and which issue-taxonomy scripts are safe to
rerun versus one-shot (§3.7). It is the *operational* companion to
[docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md),
which owns the 8-stage apply/validate/audit mechanics and should not be
re-derived from this doc.

**Known/likely misuse:**
- Treating this runbook as authoritative for the `updateByLine` /
  XML-validation stages themselves — those gotchas live only in
  `correction-workflow.md` §8; this doc intentionally does not duplicate them.
- Rerunning the one-shot `csl-corrections_label.py` / `_project.py` /
  `csl-orig_label.py` / `_project.py` backfill scripts as if they were the
  general-purpose issue-taxonomy verifiers (§3.7 table) — they carry hardcoded
  2026-backfill issue lists and are not idempotent maintenance tools.
- Applying an old correction issue without running the §3.2 preflight grep
  first — the registry's "No change required" verdict is binding until a
  maintainer reopens the item; skipping preflight risks reintroducing a
  rejected change.
- Reading the top-level `app/` PHP tree as a locally runnable app — it is the
  deployed Cologne-server source, not executable from this repo (§2).
- Treating script line counts in the maintainer appendix (§6) or here as a
  quality/complexity measure — they are stale-drift identifiers, not metrics.

## Maintenance & sunset plan

Owned by the `csl-corrections` repo itself: the daily-cron workflow
([.github/workflows/fetch-daily-corrections-from-cologne.yml](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/.github/workflows/fetch-daily-corrections-from-cologne.yml))
is the automated writer, and any human maintainer applying a batch or touching
the cron/batch-folder convention is bound by this doc's own "Maintenance
rule" above to update §1/§3 in the same PR. No dedicated human owner beyond
"whoever operates a `csl-corrections` batch round" — there is no separate
pipeline or service to page. **What "archived/ended" looks like:** the
runbook is retired only if the batch-processing model it documents is retired
— e.g. the Cologne form intake is replaced, or `csl-orig` correction delivery
moves off the change-file/`updateByLine` mechanism entirely. Short of that,
the doc ages in place per its own "Known limitations" section (cron/schedule
drift, historical §3.5 scripts going further out of date) rather than being
sunset.

## Deprecation status

`active`

## Related documents

[correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) ·
[CLAUDE.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/CLAUDE.md) ·
[HYPOTHESES_AND_VIZ_MEMO.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/HYPOTHESES_AND_VIZ_MEMO.md) ·
[README.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/README.md)

## Revision history

| Date | Change | By |
|---|---|---|
| 10-07-2026 | Initial version + README link | Fable 5 (`claude-fable-5`), H502 |
| 11-07-2026 | template v2 backfill (H663) | Sonnet 5 (`claude-sonnet-5`) |

_Dr. Mārcis Gasūns_
