# batch_pending durability — never leave validated changefiles local-only

_Created: 01-08-2026 · Last updated: 01-08-2026_

**Why this exists (H2086):** agent-validated `updateByLine` changefiles for the next
monthly csl-orig batch sit in `batch_pending/`. If they are only on one machine,
a wipe or worktree GC loses work that already passed XML validation. The queue
must be **git-tracked and pushed** the same pass it is filled.

## Contract

| Rule | Detail |
|---|---|
| **Track** | Every file under `batch_pending/` (except editor junk) is **committed** to this repo. |
| **Push** | Same session: `git push` (or PR) so `origin` has the queue. Local-only = failed. |
| **Drain** | Monthly `/cologne-batch-pr` moves items into `batch_YYYYMMDD/` and opens the csl-orig PR. |
| **Never** | Direct-push corrections into `csl-orig` between batches; no noise PR stream. |
| **Validate** | Windows: `make_xml.py` “All records parsed by ET” is the local gate (full `xmlchk` on XAMPP when available). |

## Operator recipe (after `/cologne-correction-queue` validates a change)

```sh
# 1. Files already written under batch_pending/dictionaries/<dict>/
# 2. Durability gate (must exit 0 before you leave the session)
python scripts/check_batch_pending_tracked.py

# 3. If untracked/uncommitted files:
git add batch_pending/
git commit -m "corrections: queue <dict> change_<dict>_N for monthly batch"
git push origin HEAD   # or open a PR on a feature branch

# 4. Re-check
python scripts/check_batch_pending_tracked.py
```

Dry inventory (always safe):

```sh
python scripts/check_batch_pending_tracked.py --list
```

## What the check proves

- Every path under `batch_pending/` (files only) is either the README or a
  changefile/readme under `dictionaries/<dict>/`.
- No **untracked** or **modified-unstaged** pending files in the working tree.
- Optional: warns if local `main` is ahead of `origin/main` with pending changes
  still unpushed (when run on `main`).

Exit **0** = durable enough for this clone. Exit **1** = agent must commit/push
before ending the session.

## Relation to other docs

- Application workflow: [correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
- Batch assembly around the workflow: [BATCH_RUNBOOK.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/BATCH_RUNBOOK.md)
- Staging pointer: [batch_pending/README.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/batch_pending/README.md)

_Dr. Mārcis Gasūns_
