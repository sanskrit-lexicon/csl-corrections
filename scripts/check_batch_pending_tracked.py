#!/usr/bin/env python3
"""Fail if batch_pending/ has untracked or uncommitted durable work (H2086).

Usage:
    python scripts/check_batch_pending_tracked.py
    python scripts/check_batch_pending_tracked.py --list
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PENDING = ROOT / "batch_pending"


def _run(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def list_pending_files() -> list[Path]:
    if not PENDING.is_dir():
        return []
    return sorted(p for p in PENDING.rglob("*") if p.is_file())


def _upstream_ref() -> str:
    """Return the tracking remote ref for the current branch (fallback: origin/main)."""
    r = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    ref = r.stdout.strip()
    if r.returncode == 0 and ref:
        return ref
    return "origin/main"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--list",
        action="store_true",
        help="print tracked/on-disk inventory and exit 0 (always safe)",
    )
    args = ap.parse_args()

    # Fetch so the upstream ref reflects current remote state before comparing.
    _run(["git", "fetch", "origin", "--quiet"])

    on_disk = list_pending_files()
    rels = [p.relative_to(ROOT).as_posix() for p in on_disk]

    tracked = _run(["git", "ls-files", "batch_pending"])
    if tracked.returncode != 0:
        print(f"FAIL git ls-files: {tracked.stderr.strip()[:300]}", file=sys.stderr)
        return 1
    tracked_set = {ln.strip().replace("\\", "/") for ln in tracked.stdout.splitlines() if ln.strip()}

    status = _run(["git", "status", "--porcelain", "--", "batch_pending"])
    if status.returncode != 0:
        print(f"FAIL git status: {status.stderr.strip()[:300]}", file=sys.stderr)
        return 1
    dirty_lines = [ln for ln in status.stdout.splitlines() if ln.strip()]

    print(f"batch_pending on disk: {len(rels)} file(s)")
    for r in rels:
        mark = "TRACKED" if r in tracked_set else "UNTRACKED"
        print(f"  [{mark}] {r}")

    if args.list:
        # --list is documented as always-exit-0; print any dirt as a note, not a failure.
        if dirty_lines:
            print("NOTE (list only): working-tree dirty under batch_pending", file=sys.stderr)
            for ln in dirty_lines:
                print(f"  {ln}", file=sys.stderr)
        print("OK (list only)")
        return 0

    problems: list[str] = []
    for r in rels:
        if r not in tracked_set:
            problems.append(f"untracked (not in git index): {r}")

    for ln in dirty_lines:
        problems.append(f"working-tree dirty under batch_pending: {ln}")

    # Unpushed commits containing batch_pending work — a FAIL, not a soft warn.
    # (H2306: was WARN+exit-0; that silently passes a local-only queue, the exact
    # durability failure H2086 exists to prevent.)
    upstream = _upstream_ref()
    ahead = _run(["git", "rev-list", "--count", f"{upstream}..HEAD"])
    if ahead.returncode == 0:
        try:
            n_ahead = int((ahead.stdout or "0").strip() or "0")
        except ValueError:
            n_ahead = 0
        if n_ahead > 0 and tracked_set:
            problems.append(
                f"HEAD is {n_ahead} commit(s) ahead of {upstream} — "
                f"push so batch_pending is off-machine durable"
            )

    if problems:
        print("FAIL — batch_pending not durable yet:", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        print(
            "Fix: git add batch_pending/ && git commit && git push "
            "(see docs/BATCH_PENDING_DURABILITY.md)",
            file=sys.stderr,
        )
        return 1

    print("OK — all batch_pending files tracked and working tree clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
