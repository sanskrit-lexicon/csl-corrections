# BATCH_RUNBOOK.md — metadoc

_Created: 10-07-2026 · Last updated: 10-07-2026_

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
[H502](https://github.com/gasyoun/Uprava/blob/main/handoffs/H502-Fable_csl-corrections_batch_processing_runbook_manual_10.07.26.md)
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

## Related documents

[correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) ·
[CLAUDE.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/CLAUDE.md) ·
[HYPOTHESES_AND_VIZ_MEMO.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/HYPOTHESES_AND_VIZ_MEMO.md) ·
[README.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/README.md)

## Revision history

| Date | Change | By |
|---|---|---|
| 10-07-2026 | Initial version + README link | Fable 5 (`claude-fable-5`), H502 |

_Dr. Mārcis Gasūns_
