"""check_no_emails.py -- fail if a correction-form TSV still carries an address.

Guard for the nightly cron (H3885): csl-corrections is public, so nothing may
be committed whose e-mail column is anything but a cfr_email_mask pseudonym.

    python scripts/check_no_emails.py cfr_ab/cfr_ab.tsv daily/20260901/*.tsv

Exit 0 = every data line's column 8 is masked (or empty). Exit 1 = at least one
address survived; the offending line numbers are reported, never the address.
"""
import glob
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from cfr_email_mask import is_masked  # noqa: E402

EMAIL_COLUMN = 7


def check_file(path):
    """Return a list of 1-based line numbers whose e-mail column is unmasked."""
    bad = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for n, line in enumerate(f, start=1):
            body = line.rstrip("\r\n")
            if not body.strip():
                continue
            if "Which Dictionary?" in body:
                continue  # header
            parts = body.split("\t")
            if len(parts) <= EMAIL_COLUMN:
                continue
            addr = parts[EMAIL_COLUMN].partition(":")[0].strip()
            if not addr:
                continue
            if not is_masked(addr):
                bad.append(n)
    return bad


def main(argv):
    paths = []
    for arg in argv:
        expanded = sorted(glob.glob(arg))
        paths.extend(expanded if expanded else [])
    if not paths:
        print("check_no_emails: nothing to check")
        return 0
    failures = 0
    for path in paths:
        if not os.path.isfile(path):
            continue
        bad = check_file(path)
        if bad:
            failures += 1
            shown = ", ".join(str(n) for n in bad[:10])
            more = "" if len(bad) <= 10 else " (and %d more)" % (len(bad) - 10)
            print("FAIL %s: %d line(s) with an unmasked e-mail column: %s%s"
                  % (path, len(bad), shown, more), file=sys.stderr)
        else:
            print("ok   %s" % path)
    if failures:
        print("Refusing to commit: run cfr_email_mask.py over the file(s) above.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
