# etymology_stats red-team rows 3–4 (H3537 sheet h3537-delta-redteam_26-08-26)

_Queued: 04-09-2026 · Prepared by OxAlpha (opencode/z-ai/glm-5.3-flash), apply handoff
[H4073](https://github.com/gasyoun/Uprava/blob/main/handoffs/H4073-OxAlpha_Uprava_apply-h3537-delta-redteam_26-08-26-decisions_04.09.26.md)_

Fenced lane: csl-orig takes **no direct agent commits/PRs** — this patch waits for the
monthly `/cologne-batch-pr`. Vote: 26/26 approve (04-09-2026), rows R3+R4, notes empty.

**Base:** csl-orig `30b2ae7b3c6619b1ac6a417a02e4af907c1dd9d4` (local == origin/main at
queueing time). `git apply --check` verified against that base. Re-verify against the
delivery base at drain time (batch_20260804/readme.txt trap #1).

Apply:

```sh
git -C <csl-orig> apply <path>/etymology_stats_rows34.patch
```

Files touched (3): `v02/etymology_stats/PAPER_DRAFT.md`, `DATASHEET.md`,
`stats_etymology.py`.

## Row R3 — «an exact-match variant moves no headline figure» (PAPER_DRAFT)

Option 1 of the sheet executed: the set-equality computation was **committed** (the
numbers below, computed 04-09-2026 from the committed per-dict TSVs with the pipeline's
own pairing rule — affix-set equality over shared `headword_slp1`), and Table 1 now
prints **both columns** (any-overlap + set-equality) with the multi-affix mechanism
named.

| pair | shared | any-overlap | set-equality |
|---|--:|--:|--:|
| VCP↔SHS | 206 | 98.5 | 86.9 |
| AP90↔AP | 178 | 100.0 | 97.2 |
| VCP↔AP | 97 | 96.9 | 79.4 |
| VCP↔AP90 | 93 | 96.8 | 76.3 |
| SKD↔AP90 | 84 | 91.7 | 86.9 |
| SKD↔VCP | 65 | 93.8 | 89.2 |
| SKD↔AP | 61 | 91.8 | 85.2 |
| AP↔SHS | 31 | 100.0 | 93.5 |
| AP90↔SHS | 27 | 96.3 | 92.6 |

Multi-affix correction: the retired text said «VCP 6.6 % of head-words, all others
less»; actual multi-affix shares: KRM **19.5 %** (44/226) > VCP 6.6 % (196/2964) >
SHS 3.3 % > Apte 3.2 % > AP 2.5 % > SKD 1.5 % > WIL 0.1 %.

Delta vs the sheet's summary: the sheet says "five of nine pairs fall below 90 %"
under set-equality; the committed-pipeline recount gives **six** (SKD↔VCP 89.2 %
is also below 90). The patch states six; the recomputation is reproducible from the
committed TSVs.

## Row R4 — strict subset redefined (PAPER_DRAFT + DATASHEET + stats_etymology.py)

Option 1 of the sheet executed: **strict drops both inferred tiers** (`nearest-root`,
audited ≈ 66–75 % precise, and `oracle-join`, audited ≈ 82.9 % per the repo's own
50-row audits). The "single sub-~100 % tier" claim is retired (23.3 % of VCP's
old-strict rows were oracle-join). Recomputed strict coverage (04-09-2026, committed
TSVs):

KRM 100.0 % · SKD 89.7 % · AP 85.5 % · AP90 83.7 % · VCP 63.6 % · SHS 41.5 %.

Code: `root_index(strict)` and the `root_capture.csv` strict computation now filter
`root_source not in (nearest-root, oracle-join)`; the dashboard footnote text updated.

## Follow-through for the batch executor (required with the apply)

1. Re-run `python v02/etymology_stats/stats_etymology.py` so the derived CSVs
   (`root_capture.csv`, `cross_dict_root_agreement_strict.csv`) and the dashboard are
   regenerated under the redefined strict; commit the regenerated CSVs in the same PR.
2. Sanity-check the regenerated `root_capture.csv` `pct_strict` column against the
   table above (KRM 100.0 / SKD 89.7 / AP 85.5 / AP90 83.7 / VCP 63.6 / SHS 41.5).
3. Note in the PR body: rows R3–R4 of review sheet `h3537-delta-redteam_26-08-26`
   (26/26 approve, 04-09-2026), prepared under Uprava H4073, fence-compliant
   (queue → monthly batch-PR, no direct csl-orig push).
