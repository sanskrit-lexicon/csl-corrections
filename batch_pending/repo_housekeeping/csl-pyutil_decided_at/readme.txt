queued 04-09-2026 — csl-pyutil: record decided_at in downloaded decisions.json

Source: fatigue remedies ADOPTED 04-09-2026 (MG, 3/3 chat card-by-card; verdict
protocol Uprava review/weekly/archive/decisions_applied_2026-09-04_voter-fatigue-remedies.md,
card 3). decisions.json currently carries no vote timestamp, so vote latency is
unmeasurable (VOTER_FATIGUE_CURVE_2026-09-04.md caveat).

Change: the download button's payload gains one field —
  decided_at: new Date().toISOString()
(base csl_pyutil/review_sheet.py, downloadBtn click handler, payload literal).
Consumers (review_decisions_watcher.py, /decisions-apply) ignore unknown keys —
additive, no reader change required. Note "decided" (int count) stays untouched.

Apply: git apply decided_at.patch against csl-pyutil main, one PR at the monthly
batch window. Validate after apply: python -c "import csl_pyutil" + regenerate any
one sheet (tools/_gen_aging_audit_sheet.py pattern) and confirm the payload line.

Base: csl-pyutil main@1e5e0b3
Status: 🔵 clean (anchor unique, additive one-liner) | OxAlpha (opencode/z-ai/glm-5.3-flash)
