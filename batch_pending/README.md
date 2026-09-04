# batch_pending — Cologne correction queue

_Created: 12-07-2026 · Last updated: 04-08-2026_

Staging area for validated csl-orig corrections awaiting the next monthly
`/cologne-batch-pr`. Drained into `batch_YYYYMMDD/` when shipped. Empty = queue clear.

Last drained: 2026-08-04 -> `batch_20260804` (csl-orig [PR #2884](https://github.com/sanskrit-lexicon/csl-orig/pull/2884), ap90 + mw72 + pwg, 57 changes).
Previously: 2026-07-12 -> `batch_20260712` (csl-orig [PR #2879](https://github.com/sanskrit-lexicon/csl-orig/pull/2879)).

## Durability (H2086) — mandatory

These files are **git-tracked and must be pushed** the same session they are
queued. Local-only pending = lost work on wipe/GC.

```sh
python scripts/check_batch_pending_tracked.py          # exit 0 required
python scripts/check_batch_pending_tracked.py --list   # inventory
```

Full recipe: [docs/BATCH_PENDING_DURABILITY.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/BATCH_PENDING_DURABILITY.md).

## Current queue (dict codes with change files)

**One repo_housekeeping item queued 04-09-2026** —
[`repo_housekeeping/etymology_stats_redteam_rows34/`](repo_housekeeping/etymology_stats_redteam_rows34/readme.txt)
(patch for csl-orig `v02/etymology_stats/` — PAPER_DRAFT set-equality column + strict
redefinition, rows R3–R4 of review sheet `h3537-delta-redteam_26-08-26`, prepared by
Uprava H4073 / OxAlpha; base `30b2ae7`; re-verify against the delivery base at drain
time). Dictionary change files: none — queue clear otherwise as of 04-08-2026:

| PR | contents |
|---|---|
| [#2884](https://github.com/sanskrit-lexicon/csl-orig/pull/2884) | ap90 (2) + mw72 (54 ins) + pwg (1) = 57 changes |
| [#2885](https://github.com/sanskrit-lexicon/csl-orig/pull/2885) | mw, 21,811 lines (`&c.` markup + phw graph) — split out because a diff that size should not ride inside a multi-dictionary batch |

Both are `@WAITING` on a maintainer merge; auto-merge is off by policy.

**Read [`batch_20260804/readme.txt`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_20260804/readme.txt) before preparing the next batch** — it records three traps this drain hit, all of which will recur:

1. **Change files are addressed to the base they were built against, and that may not be `origin/main`.** The mw files were prepared on a branch; 20,618 of 21,817 records failed against `main` after five upstream July commits shifted line numbers. Always re-verify every record against the *delivery* base, never the working tree.
2. **A rule-shaped change should be regenerated, not line-shifted** — and the regenerated rule must first be proven to reproduce the approved change file byte-for-byte on its own base.
3. **`updateByLine.py` doubles the carriage return on Windows**, rewriting every line in the diff. Read and write with `newline=''`.