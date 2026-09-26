"""cfr_email_mask.py -- pseudonymise the e-mail column of correction-form TSVs.

The correction form's last tab-column ("Your Email Address") is a real address,
optionally followed by ':<status>' added by a maintainer, e.g.

    someone@example.org:DONE

csl-corrections is a PUBLIC repository and the nightly cron commits these TSVs,
so the address must never reach a commit.  Every consumer (cfr_adj.py,
scripts/update_cfr_ab.py) routes the column through mask_email_field() below,
which keeps the ':<status>' suffix intact -- downstream code depends on it --
and replaces the address itself with a stable pseudonym:

    user_<12 hex>:DONE

The pseudonym is HMAC-SHA256(salt, lowercased address), so the same submitter
keeps the same id across days and across files, and correction threads stay
followable without publishing anyone's address.

Salt: the CFR_EMAIL_SALT environment variable when set (secret in the workflow),
otherwise DEFAULT_SALT below.  With the default salt the mapping is guessable by
anyone who already knows an address, so it is a publication guard, not a
cryptographic one -- set the secret if that matters.
"""
import hmac
import hashlib
import os

DEFAULT_SALT = "csl-corrections/public-pseudonym/v1"
PSEUDONYM_PREFIX = "user_"
PSEUDONYM_HEXLEN = 12


def _salt():
    return os.environ.get("CFR_EMAIL_SALT") or DEFAULT_SALT


def pseudonym(address):
    """Stable, non-reversible id for one address. '' stays ''."""
    address = (address or "").strip()
    if not address:
        return ""
    digest = hmac.new(
        _salt().encode("utf-8"),
        address.lower().encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return "%s%s" % (PSEUDONYM_PREFIX, digest[:PSEUDONYM_HEXLEN])


def is_masked(value):
    """True when value already carries a pseudonym rather than an address."""
    value = (value or "").strip()
    if not value.startswith(PSEUDONYM_PREFIX):
        return False
    hexpart = value[len(PSEUDONYM_PREFIX):]
    if len(hexpart) != PSEUDONYM_HEXLEN:
        return False
    try:
        int(hexpart, 16)
    except ValueError:
        return False
    return True


def mask_email_field(field):
    """Mask '<address>[:<status>]', preserving the status suffix verbatim."""
    if field is None:
        return ""
    stripped = field.strip()
    if not stripped:
        return field
    addr, sep, status = stripped.partition(":")
    if is_masked(addr):
        return stripped  # already masked; idempotent
    return pseudonym(addr) + sep + status


def mask_tsv_line(line, column=7):
    """Mask column `column` (0-based) of one tab-separated line.

    Lines with too few columns, blank lines and the header row are returned
    unchanged -- shape validation is the caller's job.
    """
    if not line.strip():
        return line
    newline = ""
    body = line
    while body.endswith("\n") or body.endswith("\r"):
        newline = body[-1] + newline
        body = body[:-1]
    parts = body.split("\t")
    if len(parts) <= column:
        return line
    if "Which Dictionary?" in body:  # header row
        return line
    parts[column] = mask_email_field(parts[column])
    return "\t".join(parts) + newline


def mask_tsv_file(path, column=7):
    """Rewrite `path` in place with the e-mail column masked.

    Returns the number of lines whose e-mail column actually changed.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    out = [mask_tsv_line(line, column) for line in lines]
    changed = sum(1 for a, b in zip(lines, out) if a != b)
    if changed:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(out)
    return changed


if __name__ == "__main__":
    import sys
    for arg in sys.argv[1:]:
        n = mask_tsv_file(arg)
        print("masked %d line(s) in %s" % (n, arg))
