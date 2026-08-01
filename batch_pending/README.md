# batch_pending — Cologne correction queue

_Created: 12-07-2026 · Last updated: 01-08-2026_

Staging area for validated csl-orig corrections awaiting the next monthly
`/cologne-batch-pr`. Drained into `batch_YYYYMMDD/` when shipped. Empty = queue clear.

Last drained: 2026-07-12 -> batch_20260712 (csl-orig PR #2879).

## Durability (H2086) — mandatory

These files are **git-tracked and must be pushed** the same session they are
queued. Local-only pending = lost work on wipe/GC.

```sh
python scripts/check_batch_pending_tracked.py          # exit 0 required
python scripts/check_batch_pending_tracked.py --list   # inventory
```

Full recipe: [docs/BATCH_PENDING_DURABILITY.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/BATCH_PENDING_DURABILITY.md).

## Current queue (dict codes with change files)

See `dictionaries/<dict>/` — ap90, mw, mw72, pwg as of the last inventory.