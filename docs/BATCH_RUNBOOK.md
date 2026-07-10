# csl-corrections — batch processing runbook

_Created: 10-07-2026 · Last updated: 10-07-2026_

The operator manual for this repository: how a correction travels from a
reader's form submission to a committed change in `csl-orig`, which script
runs when, and what each folder means. Written so a **new operator can run the
repo from this document alone** (H502, Fable 5 `claude-fable-5`; every command,
path and count below was read from the scripts and data on 10-07-2026, not
recalled). The org-wide 8-stage *application* workflow (snapshot →
`updateByLine` → validate → audit → commit) is owned by
[docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
— this runbook covers everything *around* it: intake, registry, batches,
derived data, and issue-taxonomy maintenance.

---

## 1. Cheat-sheet — the whole pipeline on one screen

```
READER            COLOGNE SERVER              THIS REPO                      csl-orig
──────            ──────────────              ─────────                      ────────
fills the   ──►   app/correction_form.php     daily CRON (00:00 UTC)
web form          responses → cfr.tsv    ──►  daily/YYYYMMDD/ + cfr_ab/cfr_ab.tsv   (automatic)
                                              │
                                              ▼ (a maintainer/corrector decides)
                                              cfr_ab.tsv verdicts: "Corrected …" /
                                              "No change required"  ◄── THE REGISTRY
                                              │
                                              ▼ (for issue-worthy items)
                                              upload_github_issue.py → GitHub issues
                                              │
                                              ▼ (a correction round is assembled)
                                              batches/YYYYMMDD/dictionaries/<dict>/
                                                change_<dict>_N.txt + readme.txt
                                              │
                                              ▼ per docs/correction-workflow.md
                                              updateByLine → validate → audit ──►  ONE consolidated PR
                                              │
                                              ▼ afterwards
                                              scripts/build_correction_loci.py --selftest
                                              scripts/build_correction_viz.py
```

Operator commands, in the order a batch actually needs them:

```sh
# 0. nothing — intake is automatic (cron); check it ran (see §3.0)
# 1. preflight an old issue against the registry (see §3.2 — grep, no script)
# 2. assemble batches/YYYYMMDD/dictionaries/<dict>/change_<dict>_N.txt + readme.txt
# 3. apply + validate per docs/correction-workflow.md (updateByLine, xmllint — owned there)
# 4. rebuild the derived layer and the figures:
python scripts/build_correction_loci.py --selftest
python scripts/build_correction_viz.py
# 5. keep the issue taxonomy clean (re-runnable):
python csl-corrections_verify.py
python count_labels.py
```

## 2. Environment & prerequisites

- **Python 3** (all scripts already carry the org UTF-8 stdio convention) and
  the **`gh` CLI, authenticated** — every issue-taxonomy script shells out to
  `gh api`.
- **Sibling checkout `../csl-orig`** — needed only when applying a batch (the
  workflow doc's stages) and when refreshing
  [data/derived/dict_entry_counts.tsv](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/data/derived/dict_entry_counts.tsv)
  (a `grep -c '^<L>'` cache kept precisely so the viz does *not* need csl-orig).
- **No server access needed or possible from here:** the intake form
  ([app/correction_form.php](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/app/correction_form.php)
  and friends) runs on the Cologne server; the `app/` copy in this repo is the
  deployed source, not a runnable local app.
- ⚠️ This is a **data-store repo with a bot writer**: the daily cron commits to
  `main` every midnight UTC. Rebase before pushing; never force-push.

## 3. The flows, step by step

### 3.0 Daily intake (automatic — know it, don't run it)

[.github/workflows/fetch-daily-corrections-from-cologne.yml](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/.github/workflows/fetch-daily-corrections-from-cologne.yml)
runs at `0 0 * * *`: it fetches the day's form responses from the Cologne
server into `daily/YYYYMMDD/` (`cfr-<date>.tsv`, `cfr-<date>-corrected.tsv`,
`correctionform-<date>.txt`, plus per-dict `dictionaries/` splits) and appends
to **[cfr_ab/cfr_ab.tsv](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/cfr_ab/cfr_ab.tsv)**,
then commits `[CRON] daily corrections for YYYY-MM-DD`. An empty `daily/`
folder for a date means a no-submissions day, not a failure. **Operator check:**
the latest `[CRON]` commit should be no older than ~24h; if it is, open the
workflow run log on GitHub.

### 3.1 The registry — `cfr_ab.tsv` and `correctionform.txt`

`cfr_ab.tsv` is the append-only ledger of every form submission **with the
corrector's verdict** in the last column (`<who>:Corrected <date>` /
`No change required`). [correctionform.txt](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/correctionform.txt)
is the human-readable master history (26,246 records, 0 pending as of
26-04-2026). Maintained by the cron +
[scripts/update_cfr_ab.py](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/scripts/update_cfr_ab.py).

### 3.2 Preflight — before applying ANY old correction issue

Verbatim policy from [CLAUDE.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/CLAUDE.md):
search this repo's CFR and batch history for the same dictionary, L-number,
headword, old and new text. If the registry records the proposal as
`No change`, rejected, or deferred — **stop** unless a maintainer reopens it.
In practice:

```sh
grep -i "<headword-or-L>" cfr_ab/cfr_ab.tsv correctionform.txt
grep -ri "<headword-or-L>" batches/ batch_*/ --include="*.txt" -l
```

Also decide (and record in the batch `readme.txt`): plain replacement, or the
inline correction layer `{{old->new||YYYYMMDD|author|issue|}}`.

### 3.3 Assembling a batch

A batch is one dated folder:

```
batches/YYYYMMDD/dictionaries/<dict>/change_<dict>_1.txt   # the change file(s)
batches/YYYYMMDD/dictionaries/<dict>/readme.txt            # issue link, scope, validation note
```

The change file carries paired records — a `; <L>…<pc>…<k1>…<k2>` locus
comment, then `NNNN old <line>` / `NNNN new <line>`, then a `;---` separator —
so the change survives re-derivation from csl-orig (see the worked example in
[README.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/README.md)).
GRA uses an inline `<chg>` dialect; both dialects are parsed by the loci
builder. The top-level `batch_YYYYMMDD/` folders (2024–mid-2026) are the same
thing in the **legacy layout** — read-only history, new rounds go under
`batches/`. Each batch readme names its source GitHub issue; per the org rule,
batches ship to csl-orig as **one consolidated PR, at most ~monthly** — never
per-word PRs.

### 3.4 Applying the batch to csl-orig

Owned entirely by
[docs/correction-workflow.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md)
(8 stages, `updateByLine.py`, XML validation, the BOM/`<LEND>`/CRLF/line-count
gotchas in its §8). Do not re-derive it from this runbook; go there.

### 3.5 Historical intake scripts (one-shot era, still legible)

- [cfr_adj.py](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/cfr_adj.py)
  (2014–2019): `python cfr_adj.py cfr.tsv correctionform.txt` — collates the
  Google-Form-era response sheet into per-dict
  `dictionaries/<dict>/<dict>_correctionform.txt`, time-sorted, skipping dicts
  with nothing new. The `dictionaries/` tree it maintains is that era's output.
- [upload_github_issue.py](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/upload_github_issue.py)
  (`python upload_github_issue.py app/correction_response/cfr.tsv`) — posts new
  cfr rows as GitHub issues, tracking the last-handled line so reruns don't
  duplicate; the `_scott` variant does the same for per-batch TSVs without the
  line tracker. Rerun only when adding a genuinely new response file.

### 3.6 Derived data + figures (after any batch lands)

```sh
python scripts/build_correction_loci.py --selftest    # → data/derived/correction_loci.tsv
python scripts/build_correction_viz.py                # → docs/img/*.svg (velocity, density, treemap)
```

`correction_loci.tsv` holds one row per correction record parsed from every
change file in both batch layouts (39,540 rows as of 07-07-2026), with
`process ∈ {bulk, human}` separating the two machine-generated markup batches
from steady human correction. `--selftest` validates the census invariants —
**a selftest failure after your batch means your change file's shape is
wrong**, fix the file, not the parser. Spec:
[docs/HYPOTHESES_AND_VIZ_MEMO.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/HYPOTHESES_AND_VIZ_MEMO.md) §5.1.

### 3.7 Issue-taxonomy maintenance (this repo + csl-orig's tracker)

Two script families, **different rerun rules**:

| Script | What | Rerun? |
|---|---|---|
| [csl-corrections_verify.py](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/csl-corrections_verify.py) | audits every issue: exactly one type label, one severity, milestone matches type | ✅ any time (read-only) |
| [count_labels.py](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/count_labels.py) | open/closed counts per type label (feeds the README table) | ✅ any time |
| [csl-orig_fetch.py](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/csl-orig_fetch.py) / `csl-orig_verify.py` | same, against csl-orig's tracker | ✅ read-only |
| [csl-corrections_label.py](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/csl-corrections_label.py) / `_project.py`, `csl-orig_label.py` / `_project.py` | **one-shot backfills** — issue numbers are hardcoded lists from the 2026 runbook pass | ⚠️ do NOT rerun blindly; new issues are labeled by hand per CLAUDE.md's taxonomy |

Milestone numbers (DTB=1, DQ=2, SD=3, ME=4 here) were **discovered from the
API, never hardcode them** for another repo.

⚠️ **Known inconsistency (flagged, not resolved here):**
[CLAUDE.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/CLAUDE.md)
documents the *tooling-repo* taxonomy (`bug/feature/…`, `trivial…critical`,
"API Stability" milestones), while the verify scripts — and the 100 issues
they audited — enforce the *dictionary-repo* taxonomy (`link-target/…`,
`minor/medium/hard`, DTB/DQ/SD/ME). The scripts reflect practice; when
labeling a new issue, follow what `csl-corrections_verify.py` checks, and
treat the CLAUDE.md section as due for correction.

## 4. Symptom → cause → cure

| Symptom | Cause | Cure |
|---|---|---|
| Push rejected on `main` | the midnight cron committed since your pull | `git pull --rebase`, push again |
| No `[CRON]` commit for >24h | the fetch workflow failed | open the Actions run log; the Cologne side occasionally times out — rerun the workflow |
| `build_correction_loci.py --selftest` fails after your batch | change file deviates from a known dialect (missing `;` separator, malformed `old`/`new` pair, wrong locus comment) | fix the change file — the invariants are the spec |
| Issue scripts print `API error` / empty pages | `gh` unauthenticated or rate-limited | `gh auth status`; wait out the rate window |
| `updateByLine` line-count mismatch / xmllint failure | see the application workflow's own gotchas | [correction-workflow.md §8](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/correction-workflow.md) |
| A "new" correction was already rejected years ago | preflight skipped | §3.2 — the registry verdict stands unless a maintainer reopens |
| Duplicate GitHub issues after an upload rerun | `upload_github_issue.py` line-tracker file was reset | check `last_cfr_line*` before rerunning; close duplicates by hand |

## 5. Glossary

- **CFR** — Correction Form Response (one reader submission; a row of `cfr*.tsv`).
- **cfr_ab.tsv** — the append-only registry of all CFRs with corrector verdicts.
- **Change file** — paired `old`/`new` line records applied by `updateByLine.py`.
- **Batch** — one dated folder of change files + readme, shipped as one PR.
- **`batches/` vs `batch_YYYYMMDD/`** — current vs legacy layout of the same thing.
- **Daily fetch** — the midnight cron pulling the Cologne form responses.
- **L-number** — csl-orig's stable per-entry ID (`<L>`); locus of every correction.
- **Print change** — the printed book itself is wrong; recorded, not "fixed" silently.
- **No change required** — registry verdict: proposal examined and declined.
- **DTB / DQ / SD / ME** — the four milestones (Dictionary to Book, Digitization
  Quality, Structured Data, Major Enhancements).

## 6. Maintainer appendix

Per-script inventory (lines as of 10-07-2026): `cfr_adj.py` 266 ·
`upload_github_issue.py` 115 / `_scott` 124 · `csl-corrections_label.py` 140 /
`_verify.py` 90 / `_project.py` 83 · `csl-orig_fetch.py` 70 / `_label.py` 176 /
`_project.py` 73 / `_verify.py` 66 · `count_labels.py` 36 ·
`validate_mermaid*.py` (workflow-doc diagram checkers). Invariants worth
defending: **cfr_ab.tsv is append-only** (verdicts are edited in place, rows
never deleted); **correctionform.txt is the master history** (the "0 PENDING"
line is the health signal); **the loci builder's selftest is the change-file
spec in executable form**; the hardcoded issue lists in the `_label`/`_project`
scripts are a historical record of the 2026 taxonomy backfill, not a template.
Observed trap: `app/` looks runnable but is the deployed Cologne-server source
— nothing in it executes locally.

_Dr. Mārcis Gasūns_
