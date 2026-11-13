_Created: 13-11-2026 · Last updated: 13-11-2026_

# BUGHUNT-FINDINGS — csl-corrections — 13.11.2026

**Repo:** [sanskrit-lexicon/csl-corrections](https://github.com/sanskrit-lexicon/csl-corrections) · **Date:** 2026-11-13 · **Mode:** nightly bug hunt (MG ruling 26-09-2026), read-only Phase 1 → report → HIGH auto-fix
**Executor:** mimo-v2.6-flash (`xiaomi-token-plan-sgp/mimo-v2.6-flash`)
**Elapsed:** ~26 min (02:52–03:18 +0300)

Scope: live code only — root `*.py`/`*.sh`, `scripts/`, `app/`, `.githooks/`, `.github/workflows/`. Skipped: vendored `batch_*/` copies of `updateByLine.py`/`transcoder.py`, lockfiles, `data/`+`daily/`+`cfr_ab/` bulk TSVs, `node_modules`. No `stenogrammy/` path was read (fence held).

## Verdict

| Severity | Count | Auto-fixed in this run |
|---|---|---|
| HIGH | 1 | 1 (PR #463) |
| MEDIUM | 6 | 0 (report-only per ruling) |
| LOW | 5 | 0 |
| Committed secrets | 0 | — |

## Findings (ranked)

### HIGH-1 — shared-main-tree pre-commit guard is a no-op on macOS/Linux (dead config wiring)

**File:** [.githooks/pre-commit:23](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/.githooks/pre-commit#L23)

`CANONICAL_MAIN_TREE="C:/Users/user/Documents/GitHub/csl-corrections"` is a Windows-authored path with no `$HOME` fallback, so on this Mac (and any Linux clone) the comparison never matches and every direct commit in the shared main tree passes. The hook is the only enforcement that binds Claude Code and Codex sessions identically against the H214/H685 tree-intermix work-loss class it was rolled out for (11-07-2026); on the platform where the sessions actually run it is dead code.

**Live evidence (executed 13-11-2026):**

```
toplevel=/users/mac/documents/github/csl-corrections
canonical=c:/users/user/documents/github/csl-corrections
NO MATCH — guard passes (dead on this platform)
```

**Prior art (same org, already fixed elsewhere):** [Uprava pre-commit](https://github.com/gasyoun/Uprava/blob/main/.githooks/pre-commit) carries a `$HOME/Documents/GitHub/Uprava` fallback alongside the Windows path; `csl-observatory/.githooks/pre-commit` uses `${HOME}/...` directly.

**Fix (this run, PR #463):** add the `$HOME`-derived canonical path as a second comparison target, mirroring the Uprava pattern; `ALLOW_MAIN_TREE_COMMIT=1` escape unchanged.

### MEDIUM-2 — Scott issue-uploader truncates its progress ledger on every success

**File:** [upload_github_issue_scott.py:114](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/upload_github_issue_scott.py#L114)

The ledger `last_cfr_line_scott.txt` is documented as one `tsvfile:count` line **per batch file**, and the reader (lines 17–24) scans all lines for the matching prefix. The success write opens it with mode `'w'`, so each successful upload rewrites the whole file with only the current tsvfile's entry. Every other batch's progress is destroyed; the next run of those files starts at `lst=0` and re-posts **all** their entries as duplicate issues to `sanskrit-lexicon/csl-orig` (the fenced upstream).

**Live evidence (executed):**

```
before: 'a.tsv:5\nb.tsv:7\n'
after : 'a.tsv:6'
b.tsv progress lost: True
```

Report-only (MEDIUM): minimal fix would be read-all → replace-one-line → rewrite; not auto-fixed per the 26-09-2026 severity gate.

### MEDIUM-3 — `cfr_adj.py` exits 0 on a malformed timestamp: nightly goes green with no output

**File:** [cfr_adj.py:96-101](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/cfr_adj.py#L96-L101)

The bare `except:` around sort-time construction ends in `exit()`, which raises `SystemExit(None)` — shell status **0**. `validate_tsv()` only counts tabs, so a tab-shaped but unparseable timestamp on any line after the header prints `ERROR time=...` and terminates the whole run successfully, before any `correctionform` file is written. `fetch_yesterday_cfr.sh` (`set -euo pipefail`) and the [daily workflow](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/.github/workflows/fetch-daily-corrections-from-cologne.yml) then report success while that day's correctionform was never regenerated; records survive in the committed TSV, so no data loss — a false-green, not a crash.

**Live evidence (executed):**

```
exit code: 0
stdout tail: ["ERROR time='not-a-date'", " b'not-a-date\\tMW\\t2\\t...'", "['not-a-date']"]
stderr: (empty)
```

Report-only: fix shape is `sys.exit(1)` (or re-raise) in that branch.

### MEDIUM-4 — `download_cfr.sh` still fetches without `-f`: HTTP error page overwrites a tracked 3 MB TSV

**File:** [download_cfr.sh:6](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/download_cfr.sh#L6)

`curl -o cfr.tsv <url>` with no `--fail` saves a 404/500 HTML page under the TSV name and exits 0 — exactly the H3885 class that was fixed in [fetch_yesterday_cfr.sh](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/fetch_yesterday_cfr.sh) (`-f`, HTTP-code branch, empty-file check) but never applied here. The victim, [app/correction_response/cfr.tsv](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/app/correction_response/cfr.tsv), is git-tracked (3 MB), so the local copy is clobbered; `cfr_adj.py`'s `validate_tsv()` downstream refuses to write outputs (that guard holds), but the source file itself is left as HTML until someone notices.

**Evidence:** script source (no `-f`/`--fail` anywhere); `git ls-files app/correction_response/cfr.tsv` → tracked.

Report-only: fix shape is the same curl stanza `fetch_yesterday_cfr.sh` already uses.

### MEDIUM-5 — `update_user_corrections.sh` reports DONE on a failed csl-orig build/push

**File:** [update_user_corrections.sh](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/update_user_corrections.sh)

No `set -e` and no exit-code checks: `generate_dict.sh`, `xmlchk_xampp.sh`, `git commit` and `git push` can each fail and the script still prints `DONE: update local installation of $dictlo`. This is the operator-facing signal on the path that pushes user corrections into fenced `csl-orig`; a swallowed push failure reads as "landed".

**Evidence:** script source — only `cd` has `|| exit 1`; every downstream command is unchecked; last line is an unconditional `echo DONE`.

Report-only: fix shape is `set -euo pipefail` (keeping the intentional `git commit`-nothing case handled).

### MEDIUM-6 — `app/gitupdate.sh` pushes a `master` branch that does not exist; caller ignores the failure

**File:** [app/gitupdate.sh:5](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/app/gitupdate.sh#L5) (invoked by [app/testgit.php](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/app/testgit.php))

`git push origin master` — but `git ls-remote --heads origin` shows **no `master` ref at all** (default branch is `main`, `origin/HEAD -> origin/main`). The push cannot succeed; `testgit.php` captures `shell_exec` output and never inspects an exit status, so the CLI "test" echoes the failure text and exits 0. The intended backup of the correction-form intake commits stays local.

**Live evidence (executed):**

```
git ls-remote --heads origin   # no refs/heads/master
git log -1 -- app/gitupdate.sh  # 2019-12-17 "trial for autoupdate"
```

Caveat: the Cologne-side clone (where this script is meant to run) could not be probed from here; the defect is proven against this repo's remote, which is the only origin the script names.

Report-only: fix shape is `git push origin HEAD` (or `main`) plus a non-zero exit on push failure.

### MEDIUM-7 — correction form sanitiser destroys decimal L-numbers and non-ASCII headwords in prefill

**File:** [app/correction_form.php:26](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/app/correction_form.php#L26) and [app/correction_form.php:37](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/correction_form.php#L37)

`preg_replace('|[^A-Za-z0-9]|','',…)` (the 2022 XSS fix) strips **every** non-alphanumeric character: decimal L-codes such as `12519.002` (which occur in the live daily TSVs) lose their dot, and IAST/Devanagari headwords lose all diacritics. The mangled value is what the user sees prefilled and what gets submitted as `entry_L`/`entry_hw`.

**Live evidence (executed, php 8):**

```
lnum in=[12519.002] out=[12519002]
hw in=[kārtsna]     out=[krtsna]
hw in=[ātmā]        out=[tm]
```

Report-only: fix shape is a whitelist that keeps `.`/`-`/combining marks while still rejecting `<>"'` (the actual XSS payload shape the 2022 comment names).

### LOW-8 — `upload_github_issue.py` POSTs to GitHub with no timeout

**File:** [upload_github_issue.py:75](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/upload_github_issue.py#L75)

`s.post(...)` has no `timeout=`; a stalled connection hangs the manual upload run indefinitely (same in [upload_github_issue_scott.py:84](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/upload_github_issue_scott.py#L84)). Not on the nightly path.

### LOW-9 — dead config map in the label verifier

**File:** [csl-corrections_verify.py:15](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/csl-corrections_verify.py#L15)

`ms_title_to_num` is defined and never referenced; the live lookup is `type_to_ms` (line 21). Dead twin invites future edits to the wrong map.

### LOW-10 — `update_cfr_ab.py` start-date filter silently bypassed for single-digit months

**File:** [scripts/update_cfr_ab.py:30](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/scripts/update_cfr_ab.py#L30)

`datetime.strptime(timestamp_str[:10], '%m/%d/%Y')` raises `ValueError` on unpadded dates (`'3/18/2014 '` — trailing space), and the `except (ValueError, IndexError)` branch **keeps** the line unconditionally. Measured: 3 192 of 26 957 rows in [cfr_ab/cfr_ab.tsv](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/cfr_ab/cfr_ab.tsv) are single-digit-month, so the `start_date` gate never applies to any of them. Benign on today's data (they are all pre-2026 legacy rows, and exact-string dedup absorbs re-adds from `daily/`), but it means a future `-corrected.tsv` replacement of such a row would leave the stale original in place forever.

**Live evidence (executed):** `'3/18/2014 14:48:54'[:10]` → `ValueError: unconverted data remains:`.

### LOW-11 — `count_labels.py` parses `gh` output without checking the exit status

**File:** [count_labels.py:14](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/count_labels.py#L14)

`json.loads(r.stdout)` runs before any returncode/stderr check; a failed `gh` call yields a raw `JSONDecodeError` traceback instead of the named API error the sibling scripts print.

### LOW-12 — committed `correction_loci.tsv` is 141 rows behind its own builder

**File:** [data/derived/correction_loci.tsv](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/data/derived/correction_loci.tsv) vs [scripts/build_correction_loci.py:189](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/scripts/build_correction_loci.py#L189)

The builder's frozen census (`EXPECTED['rows'] = 61571`) passes `--selftest`, but the committed artifact holds 61 430 rows (`git show HEAD:… | wc -l` → 61 431 lines incl. header). The 141-row delta is exactly the tracked `batch_pending/dictionaries/pw/change_pw_h3152_link_splitting.txt` rows the builder now reads and the last refresh (#356) predates. Nothing gates artifact-vs-builder freshness — the selftest asserts the builder, not the file — so the published TSV silently lags. (The shared main checkout already carries this same +141 regeneration as uncommitted WIP from another session; left untouched here.)

### Secrets scan — clean

Grepped all `*.py`/`*.sh`/`*.php`/`*.yml` for `password|secret|api[_-]?key|token|BEGIN … PRIVATE KEY`: only environment-variable reads (`GITHUB_ACCESS_TOKEN`, `${{ secrets.GITHUB_TOKEN }}`) and commented-out legacy lines. **No committed credentials.** No money rows in this repo (no GTD `@DO` minted on that axis).

## What verified green (executed this run)

- `python3 -m py_compile` over every root `*.py`, `scripts/*.py`, `app/correction_response/issue91/*.py` — clean, zero diagnostics.
- `python3 scripts/build_correction_loci.py --selftest` — SELFTEST OK (census invariants + 100 % `<pc>` header coverage hold).
- `python3 scripts/changelog_duplicate_bullets.py` — `CHANGELOG.md: no duplicated entries`.
- `python3 scripts/changelog_released_headings.py` — `CHANGELOG.md: no released heading removed (vs HEAD)`.
- Committed-secrets grep (above) — 0 hits.
- Full Python AST/file read-through of `scripts/` (incl. the 2 072-line stale-base guard main path), root pipeline scripts, `.githooks/pre-push`, `.githooks/pre-commit`, both daily workflows, and the PHP intake pair.

## Auto-fix executed (Phase 3, HIGH only)

- **HIGH-1 fixed** in PR #463: `$HOME`-derived canonical main-tree target added to [.githooks/pre-commit](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/.githooks/pre-commit), mirroring the Uprava pattern. Verification: post-fix hook run in the shared main tree → `BLOCKED` (exit 1); same hook run inside a worktree → exit 0 (worktrees unaffected, as designed); `bash -n` syntax check green. Attempt count: 1/3.
- MEDIUM/LOW findings: report-only, no code edits (per MG ruling 26-09-2026).
- No HIGH credential/infra finding was found, so no GTD row was minted on that clause.

_Dr. Mārcis Gasūns_
