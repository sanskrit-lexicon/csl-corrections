# Plan — csl-corrections interconnection, 2026-08

_Created: 26-08-2026 · Last updated: 27-08-2026_

csl-corrections's slice of the spine-interconnection programme. Programme index:
[PLAN_SPINE_INTERCONNECTION_2026H2.md](https://github.com/gasyoun/Uprava/blob/main/docs/PLAN_SPINE_INTERCONNECTION_2026H2.md).

Architecture and verification are **not** restated here (ruling F13) — they are identical for
all fourteen repos and live once in Uprava:

- [ARCHITECTURE_SPINE_INTERCONNECTION.md](https://github.com/gasyoun/Uprava/blob/main/docs/ARCHITECTURE_SPINE_INTERCONNECTION.md) — the five attachment points and the rules governing them
- [IMPLEMENTATION_SPINE_INTERCONNECTION_W1.md](https://github.com/gasyoun/Uprava/blob/main/docs/IMPLEMENTATION_SPINE_INTERCONNECTION_W1.md) — execution order, per-handoff steps, isolation, risks
- [VERIFICATION_SPINE_INTERCONNECTION.md](https://github.com/gasyoun/Uprava/blob/main/docs/VERIFICATION_SPINE_INTERCONNECTION.md) — the five gates and what "done" means

**Executed 27-08-2026** by Opus 5 (`claude-opus-5`) — see *Outcome* below. The plan is kept as the
record of what was intended and what actually happened.

## Why csl-corrections is in scope

Zero SHARED_CODE rows and no ROADMAP_INDEX row, yet it is the **only sanctioned route** into the fenced `csl-orig`, and two skills depend on it. The row documents an existing contract rather than proposing one.

## Measured baseline and target

| | Value |
|---|---|
| Wiring score, 26-08-2026 | **36** / 100 |
| Target after this plan | **40** / 100 |
| How the target is reached | ~+4 as SHARED_CODE and PROJECT_INTERLINKS presence rise. A small number for a row that protects the most fenced repo in the org. |

Measured by [`tools/interconnection_audit.py`](https://github.com/gasyoun/Uprava/blob/main/tools/interconnection_audit.py); full row in
[data/interconnection_audit_2026-08-26.json](https://github.com/gasyoun/Uprava/blob/main/data/interconnection_audit_2026-08-26.json);
report [AUDIT_REPO_INTERCONNECTION_2026-08-26.md](https://github.com/gasyoun/Uprava/blob/main/docs/AUDIT_REPO_INTERCONNECTION_2026-08-26.md).

The score counts artefacts, not whether they are true. It is **report-only** by ruling F2 and no
handoff closes on it — verification Gates 2 to 4 are what actually decide, and Gate 4 is read by
a human.

## Rulings that apply here

| Fork | Ruling |
|---|---|
| F8 | The csl-corrections bridge, the SanskritKaraoke exporter and the RuWritingStyles pipeline all become SHARED_CODE families. |
| F1 | Local `FINDINGS.md` in exactly four repos; the other eight get a `CLAUDE.md` pointer line. No repo gains the other seven registries. |

Full rulings table with every fork:
[ASK_BATCH_STAGING_REPO_INTERCONNECTION_2026-08.md](https://github.com/gasyoun/Uprava/blob/main/ASK_BATCH_STAGING_REPO_INTERCONNECTION_2026-08.md) Phase 2.

## What this plan does

1. Register the correction-queue to batch-PR bridge as a SHARED_CODE family, naming the canonical path and the reuse rule (F8).
2. State the fence explicitly in the row: agents never commit or push directly to `csl-orig`; change files here are an audit trail and are not applied at generation time; delivery is one consolidated PR at most roughly monthly.
3. Add the `CLAUDE.md` pointer line (F1). Nothing in this work touches `csl-orig`.

## Outcome — 27-08-2026

Of the three intended changes, one landed here and two were already satisfied by a sibling handoff
that a human launched ahead of this one.

| Planned | What happened |
|---|---|
| 1. Register the queue-to-batch-PR bridge as an F8 SHARED_CODE family | **Already landed** as row 27 of [SHARED_CODE.md](https://github.com/gasyoun/github-spine/blob/main/SHARED_CODE.md) by [H3561](https://github.com/gasyoun/github-spine/pull/127), written from the shipped code rather than from this spec. Verified line by line against this handoff's acceptance and **not re-added** — a second row for one canonical source is a duplicate, not an adjacent row to keep. |
| 2. State the fence explicitly in the row | **Already stated.** Row 27's rule column carries all three clauses: agents never commit or push to the fenced upstream and never open a small per-correction PR; change files here are an audit trail, not applied at generation time; delivery is one consolidated PR at most roughly monthly. No enrichment was owed — unlike [H3570](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3570-Opus_SanskritKaraoke_interconnect-karaoke-timing-caption-family_26.08.26.md), which found row 28 missing a fact and added it. |
| 3. Ruling-F1 `CLAUDE.md` pointer line, no registry files | **Shipped** ([#376](https://github.com/sanskrit-lexicon/csl-corrections/pull/376)): infra and process gotchas go to [Uprava/FINDINGS.md](https://github.com/gasyoun/Uprava/blob/main/FINDINGS.md), Sanskrit data to [SanskritLexicography/FINDINGS.md](https://github.com/gasyoun/SanskritLexicography/blob/master/FINDINGS.md), this repo keeps no registries of its own, and the line names family row 27. |

No README wiring section was owed — the 26-08-2026 audit row lists rulings F8 and F1 only, not
default F11, and the [README](https://github.com/sanskrit-lexicon/csl-corrections/blob/main/README.md)
already answers Gate 4's three questions in its opening paragraph and *Repository role* list.

**Nothing in this pass touched the fenced upstream.** The two merged diffs contain five files —
`CLAUDE.md`, `.ai_state.md`, `CHANGELOG.md` and the two interconnection docs — no change file and no
batch folder among them.

## Handoff

- [H3571 (Opus 5) — interconnect cslcorrections batchpr bridge family](https://github.com/gasyoun/Uprava/blob/main/handoffs/H3571-Opus_csl-corrections_interconnect-cslcorrections-batchpr-bridge-family_26.08.26.md) · medium · ✅ done 27-08-2026

## Autonomy contract

The launching agent may create the files named above, add hub rows, open and merge its PR,
remove its worktree and close its handoff row — without asking.

It must stop and ask if a local `FINDINGS.md` cannot be given two genuine findings (the
documented fallback is to drop the file and take the pointer line, recorded not silent), if a
corpus row would carry an unmasked snapshot or quote a sample, or if a second speculative edge
becomes necessary. It must never turn the wiring score into a failing gate, commit to
`csl-orig`, or add the seven non-FINDINGS registries.

## Open @DECIDE

None. Every fork touching csl-corrections was ruled in sitting 1 on 26-08-2026, so the autonomy gate
passes and nothing in the wave-1 path stalls on a human.

_Dr. Mārcis Gasūns_
