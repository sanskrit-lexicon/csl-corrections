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

**`mw` only, and it is BLOCKED — do not ship it as staged (04-08-2026).**

`change_mw_1.txt` (21,791 bare `&c.` → `<ab>&c.</ab>`, approved on
[MWS#86](https://github.com/sanskrit-lexicon/MWS/issues/86)) and `change_mw_2.txt`
(26 phw-graph pointer fixes) are addressed to a base that is **not** csl-orig
`origin/main`: **20,618 of 21,817 records fail** against it. Five upstream July
correction commits (`de8c1862`, `d649aee8`, `921c916f`, `54e06384`, `4b0fdecd`)
net-deleted one line at 59923, shifting every later line number by one, and changed
content at the divergence (`alAtaSanti` → `alAtaSAnti`).

They need **content-relocation onto `origin/main` plus a fresh XML gate** — the
"All records parsed by ET" recorded when they were queued was measured on the wrong
base and does not transfer. Tracked as Uprava **H2270**.

Everything else that was queued shipped on 04-08-2026; see
[`batch_20260804/readme.txt`](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_20260804/readme.txt)
for the validation method (isolated build, **no swap window**) and for why
`change_ap90_1.txt` was dropped as a duplicate of an edit already in PR #2879.