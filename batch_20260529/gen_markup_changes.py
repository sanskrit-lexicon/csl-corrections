# coding=utf-8
"""gen_markup_changes.py
Generate audit-trail change files for markup fixes applied 2026-05 to csl-orig.

For each dictionary, extracts the pre-fix version from git, then runs
diff_to_changes_dict.py to produce a updateByLine-format change file.

Run from: csl-corrections/batch_20260529/
Requires: git, diff_to_changes_dict.py (copied into each dict subdir)

Usage:
  python gen_markup_changes.py
"""
from __future__ import print_function
import sys, os, subprocess, shutil, codecs

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

# Mapping: dict_code -> (commit_sha_of_our_fix, csl_orig_parent_path)
# The "before" is the parent of the fix commit; "after" is current csl-orig.
DICT_COMMITS = {
    'bor':  '442e0d7',
    'ap90': '863d559',
    'gra':  'a74c199',
    'mw':   '8b051ab',
    'ap':   '51a764b',
    'bur':  '969e0b8',
    'inm':  '969e0b8',
    'krm':  '969e0b8',
    'bop':  '3f53192',
    'mw72': '3f53192',
}

CSL_ORIG = 'C:/Users/user/Documents/GitHub/csl-orig'
DIFF_SCRIPT = 'C:/Users/user/Documents/GitHub/csl-corrections/batch_20250418/dictionaries/mw/diff_to_changes_dict.py'

def run(cmd, **kw):
    result = subprocess.run(cmd, shell=True, capture_output=True,
                            encoding='utf-8', errors='replace', **kw)
    return result.stdout.strip(), result.stderr.strip(), result.returncode

def extract_before(dictlo, commit_sha, outfile):
    """Extract the pre-fix version of dict.txt from git (parent of fix commit)."""
    git_ref = f'{commit_sha}^:v02/{dictlo}/{dictlo}.txt'
    cmd = f'git -C "{CSL_ORIG}" show "{git_ref}"'
    result = subprocess.run(cmd, shell=True, capture_output=True)
    if result.returncode != 0:
        print(f'  ERROR extracting {git_ref}: {result.stderr.decode()}')
        return False
    with open(outfile, 'wb') as f:
        f.write(result.stdout)
    print(f'  extracted before: {os.path.basename(outfile)} ({len(result.stdout.splitlines())} lines)')
    return True

def main():
    basedir = os.path.dirname(os.path.abspath(__file__))

    for dictlo, commit in DICT_COMMITS.items():
        dictdir = os.path.join(basedir, 'dictionaries', dictlo)
        print(f'\n=== {dictlo.upper()} (fix commit {commit}) ===')

        before_file = os.path.join(dictdir, f'temp_{dictlo}_0.txt')
        after_file = f'{CSL_ORIG}/v02/{dictlo}/{dictlo}.txt'
        change_file = os.path.join(dictdir, f'change_{dictlo}_markup_1.txt')

        # Extract "before" from git
        if not extract_before(dictlo, commit, before_file):
            continue

        # Verify "after" exists
        if not os.path.exists(after_file):
            # Try Windows path
            after_file_win = after_file.replace('/c/', 'C:/').replace('/', '\\')
            if os.path.exists(after_file_win):
                after_file = after_file_win
            else:
                print(f'  ERROR: after file not found: {after_file}')
                continue

        # Run diff_to_changes_dict.py
        cmd = f'python "{DIFF_SCRIPT}" "{before_file}" "{after_file}" "{change_file}"'
        stdout, stderr, rc = run(cmd)
        if stdout:
            print(f'  {stdout}')
        if stderr:
            print(f'  STDERR: {stderr}')
        if rc != 0:
            print(f'  ERROR: exit code {rc}')

        # Clean up temp "before" file (it's large and derivable from git)
        os.remove(before_file)
        print(f'  removed temp before file')

if __name__ == '__main__':
    main()
