# Pipeline audit — csl-orig correction queue → monthly batch PR (Fable lane, H2022)

_Created: 06-08-2026 · Last updated: 06-08-2026_

**Executor:** Fable 5 (`claude-fable-5`), Claude Code. Skill: [/pipeline-audit](https://github.com/gasyoun/claude-config/blob/main/commands/pipeline-audit.md).
**Handoff:** [H2022](https://github.com/gasyoun/Uprava/blob/main/handoffs/H2022-Fable_Uprava_pipeline-hygiene-audit-non-pwg_31.07.26.md) — non-PWG pipeline hygiene audits.
**Dual-run:** independent second lane against the Grok 4.5 (`grok-4.5`) audit of 01-08-2026 and its shipped fix [csl-corrections #328](https://github.com/sanskrit-lexicon/csl-corrections/pull/328). This lane audited the **post-fix** code and did not read the Grok memo before forming its own findings.

Audit-only: no pipeline stage was patched by this pass.

---

## 1. The real call graph

The pipeline has two LLM-executed stages and three script stages. The LLM stages are stages, not documentation — they are where most of the enforcement actually lives, and where most of the gaps below sit.

| # | Stage | Driver | Reads | Writes |
|---|---|---|---|---|
| 1 | Obtain change file | [/cologne-correction-queue](https://github.com/gasyoun/claude-config/blob/main/commands/cologne-correction-queue.md) Phase 1 | issue body via `gh`, `csl-orig/v02/<dict>/<dict>.txt`, existing `batch_pending/`, CFR + batch history | scratch change file |
| 2 | Validate on a snapshot | same skill, Phase 2 | `csl-orig` working tree, `csl-pywork/v02/makotemplates/pywork/updateByLine.py`, `make_xml.py` | scratchpad temps; **temporarily overwrites `csl-orig/v02/<dict>/<dict>.txt`** |
| 3 | Park in queue | same skill, Phase 3 | — | `batch_pending/dictionaries/<dict>/change_<dict>_<seq>.txt` + `readme.txt` |
| 3b | Durability gate | [scripts/check_batch_pending_tracked.py](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/scripts/check_batch_pending_tracked.py) (H2086) | `git ls-files`, `git status`, `git rev-list origin/main..HEAD` | stdout verdict only |
| 4 | Monthly drain | [/cologne-batch-pr](https://github.com/gasyoun/claude-config/blob/main/commands/cologne-batch-pr.md) | `batch_pending/`, `git show origin/main:v02/<dict>/<dict>.txt` | branch `batch/YYYYMM-corrections` on csl-orig; ONE PR |
| 5 | Promote audit trail | same skill, Phase 4 | `batch_pending/` | `batch_YYYYMMDD/dictionaries/<dict>/`, empty `batch_pending/` |
| 6 | Public refresh | `redo_xampp_selective.sh` cron, Cologne server | merged `csl-orig` | regenerated installations |

**State at audit time (06-08-2026).** Queue empty — `batch_pending/` holds only its `README.md`, tracked and clean; `check_batch_pending_tracked.py` exits 0. Last drain was 04-08-2026 into `batch_20260804/dictionaries/{ap90,mw,mw72,pwg}` (commits `5a4a971`, `f49af36`), shipping csl-orig PRs #2884 and #2885; #2885 (mw, 21,811 lines) was still **OPEN** — the maintainer merge is correctly `@WAITING`, not a stall in our half. The local main-tree clone was **2 commits behind `origin/main`** when this audit began, which is itself the base-staleness class the pipeline keeps hitting.

---

## 2. Doc-vs-code divergences

The critical finding of this lane is not a code defect. It is that **the durability contract and the skill that fills the queue now say opposite things**, and the skill is what executes.

| # | Claim | Contradicted by | Consequence |
|---|---|---|---|
| **D1** | [docs/BATCH_PENDING_DURABILITY.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/BATCH_PENDING_DURABILITY.md) contract table: every file under `batch_pending/` is **committed**, and pushed the **same session** — "Local-only = failed." | `/cologne-correction-queue` Phase 3, final paragraph: "Do NOT commit or push csl-corrections here — the queue stays local until `/cologne-batch-pr` promotes it … (If the machine is at risk, a local commit on a `batch-pending` branch is acceptable; **never push it**.)" | The H2086 fix landed a doc and a checker but **never updated the stage that fills the queue**. An agent following the skill verbatim still parks the work local-only and is explicitly told not to push — exactly the loss the fix was for. The checker only runs if someone remembers to run it, and nothing in the skill says to. |
| **D2** | `/cologne-batch-pr` Phase 2 step 5: "**Do not** copy the corrected text into `csl-orig` and restore it afterwards — a failed restore corrupts canonical data." Builds an isolated tree instead. | `/cologne-correction-queue` Phase 2: "temporarily copy `temp_<dict>_1.txt` into `csl-orig/v02/<dict>/<dict>.txt`, run `make_xml.py` …, then **restore the snapshot immediately**". | The queue stage still mandates the swap window that the drain stage bans by name. Every queued correction opens a write window on canonical data; a crash, a hook block, or a concurrent session inside that window leaves modified canonical text behind. The two skills disagree about the single most dangerous operation in the pipeline. |
| **D3** | `/cologne-batch-pr` Phase 2 step 1: verify against the **delivery base** `git show origin/main:…`, never the working tree — with the measured 04-08-2026 result **20,618 of 21,817 records failed** against `origin/main` after passing 21,875/21,875 against the working tree. | `/cologne-correction-queue` Phase 2 step 1 snapshots from the working tree (`Copy-Item …\csl-orig\v02\<dict>\<dict>.txt`) with no `git fetch` and no base assertion. | Queue-time validation is green against whatever the local clone happens to be — a feature branch, or a clone days behind. The pipeline already **measured** this failure at drain time; the queue stage that produces the records has not been taught it. |
| **D4** | `/cologne-batch-pr` Phase 2 step 4: `updateByLine.py` is **byte-unsafe on Windows** — it doubles the carriage return, +1 byte/line, measured +273,723 bytes over 273,715 ap90 lines; read and write with `newline=''`. | `/cologne-correction-queue` Phase 2 invokes the same `updateByLine.py` with no `newline=''` guidance and no diff-size sanity check. Its only byte-level gate is the 3-byte BOM check. | A queue-time validation can pass (BOM clean, "All records parsed by ET") on a file in which **every line** was silently rewritten. The BOM check looks at bytes 0–2; CR doubling touches bytes everywhere else. |

D2–D4 share one shape: the drain skill learned three hard lessons and wrote them down; the queue skill that feeds it was never updated. The pipeline's knowledge is real but is stored in the wrong stage — the last one, not the first.

---

## 3. Silent-failure census

| # | Location | Class | What is lost when it fires | Observed / hypothetical |
|---|---|---|---|---|
| 1 | `/cologne-correction-queue` Phase 3, last paragraph | instruction that defeats its own durability gate | Validated changefiles stay on one machine; a wipe or worktree GC loses agent-validated work that already passed XML validation | observed-class (the H2086 motivation, still live in the executed stage) |
| 2 | [check_batch_pending_tracked.py:82-93](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/scripts/check_batch_pending_tracked.py) | warn-not-fail | Commits ahead of `origin/main` produce a stderr `WARN` and the function still `return 0`. A committed-but-unpushed queue passes the durability gate that exists specifically to prove off-machine durability. "Push … Local-only = failed" is documented but not enforced | observed |
| 3 | check_batch_pending_tracked.py:82 | stale comparison, no fetch | `git rev-list --count origin/main..HEAD` is computed against whatever `origin/main` the clone last fetched. This audit found the clone 2 commits behind; a queue pushed to a *stale* remote ref reads as durable | observed |
| 4 | check_batch_pending_tracked.py:82 | wrong base off `main` | The ahead-count is hardcoded to `origin/main`. On the `batch-pending` branch the skill itself suggests, the count includes every unrelated commit, so the warn is noise and gets ignored | hypothetical |
| 5 | check_batch_pending_tracked.py:68-70 | flag does not do what it documents | `--list` is documented (line 5 and BATCH_PENDING_DURABILITY.md) as "print inventory and exit 0", but returns 0 **only** when the tree is clean; with dirty files it falls through and exits 1. The one command described as "always safe" is the one that fails when there is something to see | observed |
| 6 | `/cologne-correction-queue` Phase 2 (swap window) | non-atomic write on canonical data | csl-orig's working tree holds corrected text between the copy and the restore. The skill's own guarantee ("byte-identical before and after") holds only if nothing interrupts | hypothetical, banned by name in the sibling skill |
| 7 | `/cologne-correction-queue` Phase 2 (`make_xml.py` gate) | partial validation reported as pass | On Windows `xmllint` is absent, so "All records parsed by ET" is the pass signal. ET parse is necessary, not sufficient — DTD/attribute-level defects pass. `correction-workflow.md` §8 states this; the queue skill records it as a caveat, not as a gate downgrade | observed (documented caveat) |
| 8 | `/cologne-correction-queue` Phase 2 + `updateByLine.py` | byte-level corruption invisible to the gate | CR doubling rewrites every line while BOM check and ET parse both stay green (D4) | observed-class (measured at drain time on ap90) |
| 9 | `/cologne-correction-queue` Phase 2 snapshot | stale base | Queue-time green against a working tree that is not the delivery base (D3) | observed (20,618/21,817 measured 04-08-2026) |
| 10 | `/cologne-batch-pr` Phase 4 | drop record depends on prose discipline | Entries discarded in Phase 2 are recorded "in the readme" by instruction only; nothing computes the dropped set, so a silently dropped correction leaves no machine-checkable trace | hypothetical |

**Upstream-noise ban — verdict: holding.** No code path in this repo pushes or opens a PR against `csl-orig`. The only sanctioned write is the topic branch in `/cologne-batch-pr` Phase 3, and `csl-orig` is otherwise touched read-only (`csl-orig_fetch.py`, the label/verify scripts). The queue skill's swap window (D2/#6) writes to the csl-orig **working tree** but never commits. The ban is a discipline, not a mechanism — there is no hook in this repo that would stop a direct push.

---

## 4. Capability inventory (honest, today)

**Can do:** prepare a line-addressed correction from an issue or a hand-written change file; validate it against a snapshot with an ET-parse gate and a BOM check without committing to csl-orig; park it in a per-dictionary queue with a dated, status-dotted readme; prove the queue is git-tracked and the tree clean (`check_batch_pending_tracked.py` exit 0); re-validate the whole queue against `origin/main` at drain time in one pass keyed to original line numbers; ship one consolidated PR per month with a per-dict table and `Closes #N` lines; promote the audit trail to a dated `batch_YYYYMMDD/`.

**Cannot do:** prove the queue is off-machine (the gate warns and passes); validate at queue time against the base it will actually ship to; detect CR doubling or any whole-file byte rewrite; run full DTD validation on Windows; produce a machine-checkable record of corrections dropped during a drain; prevent a direct push to `csl-orig` by any mechanism other than instruction.

---

## 5. Ranked gap specs

1. **Update `/cologne-correction-queue` Phase 3 to the H2086 contract.** Replace "Do NOT commit or push … never push it" with: commit `batch_pending/` and push in the same pass, then run `python scripts/check_batch_pending_tracked.py` and require exit 0 before the session ends. *Verify:* the skill text and [BATCH_PENDING_DURABILITY.md](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/docs/BATCH_PENDING_DURABILITY.md) no longer contradict; a queue session ends with the change file present on `origin`.
2. **Make the durability gate fail on unpushed.** `check_batch_pending_tracked.py:82-93` — fetch first, compare against the tracking branch rather than hardcoded `origin/main`, and turn the ahead-count from `WARN`+`return 0` into a problem row. *Verify:* commit a pending file without pushing ⇒ exit 1 naming the unpushed commit; push ⇒ exit 0.
3. **Carry the delivery-base rule into the queue stage.** `/cologne-correction-queue` Phase 2 — snapshot from `git show origin/main:v02/<dict>/<dict>.txt` after `git fetch`, not from the working tree, and record the base SHA in the queue `readme.txt` line so the drain can tell how far the base has moved. *Verify:* a queue run on a clone parked on a feature branch produces records that still validate at drain time.
4. **Close the swap window at queue time.** `/cologne-correction-queue` Phase 2 — adopt the drain skill's isolated-tree recipe (`generate_orig.sh` → stage corrected text → `generate_pywork.sh` → `redo_hw.sh`/`redo_xml.sh`) so csl-orig is never written to. *Verify:* a queue run leaves `git -C csl-orig status` clean at every point, not just at the end.
5. **Add a byte-shape assertion to the queue gate.** After `updateByLine.py`, require `newline=''` handling and assert output size ≈ input size + intended delta, and that the diff line count equals the intended edit count. *Verify:* a deliberately CR-doubled run fails the gate instead of passing BOM + ET.
6. **Make drops machine-visible.** `/cologne-batch-pr` Phase 4 — emit a `dropped.json` (record, reason, upstream SHA) alongside the promoted batch. *Verify:* a drain that drops a record leaves a file naming it; an empty drop set leaves an empty list, not an absent file.

Specs 1–3 are the load-bearing ones: each closes a case where the pipeline already *knows* the answer and stores it in the wrong stage.

---

## 6. Dual-run adjudication vs the Grok 4.5 lane

Comparison against [PIPELINE_AUDIT_CSL_ORIG_QUEUE_01-08-2026.md](https://github.com/gasyoun/Uprava/blob/main/docs/PIPELINE_AUDIT_CSL_ORIG_QUEUE_01-08-2026.md) (Grok 4.5, `grok-4.5`) and its shipped fix [#328](https://github.com/sanskrit-lexicon/csl-corrections/pull/328), read only after this lane's findings were formed. Classes per [/dual-run-salvage](https://github.com/gasyoun/claude-config/blob/main/commands/dual-run-salvage.md).

| Grok finding | Class | Adjudication |
|---|---|---|
| `batch_pending` local-only ⇒ machine wipe loses validated work | **conflicting (partially fixed)** | The fix shipped a doc + checker but left the filling stage instructing the opposite (D1) and the checker passing on unpushed (#2). Keep Grok's diagnosis; this lane's specs 1–2 are the completion. The gap was reported closed and is not. |
| Windows ET parse ≠ full `xmlchk` (DTD issues missed) | **identical** | Confirmed at `/cologne-correction-queue` Phase 2 and `correction-workflow.md` §8. No change. |
| BOM `utf-8-sig` write poisons the first line | **equivalent, narrower than the real risk** | The BOM class is already guarded (skill Phase 1 mandates `encoding='utf-8'`; the check runs on output). The larger unguarded byte risk on the same stage is CR doubling (D4, #8) — it rewrites every line and passes both existing gates. |
| — | **net-new (this lane)** | D2 swap window on canonical data, banned by the sibling skill but still mandated at queue time. |
| — | **net-new (this lane)** | D3 queue-time validation against the working tree instead of the delivery base, the class already measured at 20,618/21,817. |
| — | **net-new (this lane)** | #3–#5 checker defects: no fetch, hardcoded `origin/main` base, `--list` exiting 1 against its own documentation. |

**Kept from both:** Grok's three findings all stand as diagnoses; two of them (ET, BOM) need no further work, and the third is reopened rather than re-litigated. **Kept from this lane:** the five net-new items above. No finding from either lane was discarded.

---

## 7. Not audited

- `csl-pywork` internals — `updateByLine.py`, `make_xml.py`, `generate_*.sh` were treated as black boxes at their documented contracts; their sources were not read this pass. The CR-doubling and ET-vs-DTD claims are carried from the drain skill's own measured record, not re-measured here.
- No correction was executed end-to-end: the queue was empty, so stages 1–3 were audited from the skill text and the last drained batch, not from a live run.
- `batch_20240616` … `batch_20260712` historical batches, `daily/`, `cfr_ab/`, `issues/`, and the `csl-corrections_*.py` label/verify/project scripts were not audited — they are the reporting and issue-labelling surface, not the correction queue.
- csl-orig PR #2884's merge state could not be read (GitHub API TLS timeout during the audit); #2885 was confirmed OPEN.
- The Cologne server side (stage 6, `redo_xampp_selective.sh` cron) is not reachable from here and was not audited.

---

_Dr. Mārcis Gasūns_
