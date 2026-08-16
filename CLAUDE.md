# CLAUDE.md

_Created: 06-05-2026 · Last updated: 16-08-2026_

`csl-corrections` is the CDSL **correction staging ground and audit trail**:
validated change-files are parked in dated batch folders here, then shipped
into [`csl-orig`](https://github.com/sanskrit-lexicon/csl-orig) as **one
consolidated pull request about once a month**. Change-files are the durable
record; they are not applied at dictionary-generation time.

Org conventions live in [`../CLAUDE.md`](https://github.com/gasyoun/github-spine/blob/main/CLAUDE.md).
Before encodings or corpus data, read the
[Sanskrit context primer](https://github.com/gasyoun/github-spine/blob/main/SANSKRIT_CONTEXT_PRIMER.md).

## How to run

Authoritative 8-stage workflow (snapshot → apply → promote → regenerate →
validate → audit → commit → refresh):
[`docs/correction-workflow.md`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md).
Operator intake / batch-folder / `cfr_ab` registry:
[`docs/BATCH_RUNBOOK.md`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/BATCH_RUNBOOK.md).

Park locally with
[`/cologne-correction-queue`](https://github.com/gasyoun/claude-config/blob/main/commands/cologne-correction-queue.md);
ship the monthly PR with
[`/cologne-batch-pr`](https://github.com/gasyoun/claude-config/blob/main/commands/cologne-batch-pr.md).

Apply a parked change-file (never edit `csl-orig` in place):

```sh
python updateByLine.py mw.txt change_mw_1.txt mw_corrected.txt
```

Rebuild the derived census and figures:

```sh
python scripts/build_correction_loci.py --selftest
python scripts/build_correction_viz.py
```

[`data/derived/correction_loci.tsv`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/data/derived/correction_loci.tsv)
is one row per correction record (parsed from every batch folder). Do not
hand-edit it.

CI: `fetch-daily-corrections-from-cologne.yml` (intake cron),
`changelog-lint.yml`, `dependabot-auto-merge.yml`.

## Preflight for old issues

Before applying any old `csl-orig` / dictionary text-correction issue, search
the CFR and batch history for the same dictionary, L number, headword, old
text, and new text. If the registry records `No change`, rejected, deferred,
or otherwise not to be applied, **stop** unless a maintainer reopens it.

Decide replacement vs inline layer
(`{{old->new||YYYYMMDD|author|issue|}}`) *before* editing. Record that
decision in the batch readme.

## Do not touch

- **Never commit or push to `csl-orig`.** Agents prepare + XML-validate
  locally and park here. Upstream Jim/Dhaval may commit there; we do not.
- `csl-orig/v02/<dict>/<dict>.txt` itself — this repo only holds change-files.
- `data/derived/*` — regenerate from scripts.
- UTF-8 BOM — write `encoding='utf-8'`, never `utf-8-sig`.

Issues use the Cologne tooling taxonomy — see
[`/cologne-issue-runbook`](https://github.com/gasyoun/claude-config/blob/main/commands/cologne-issue-runbook.md).
Do not recopy type/severity/milestone tables into this file.

Danger facts:
[Uprava DANGER_FACTS.md](https://github.com/gasyoun/Uprava/blob/main/DANGER_FACTS.md)
and the generated block of
[AGENTS.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/AGENTS.md).

_Dr. Mārcis Gasūns_
