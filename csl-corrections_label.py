import subprocess, json, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ORG = 'sanskrit-lexicon'
REPO = 'csl-corrections'

# Milestone map (fetched from API: DTB=1, DQ=2, SD=3, ME=4)
ms_map = {
    'link-target':        1,
    'link-splitting':     1,
    'text-correction':    2,
    'encoding':           2,
    'bug':                2,
    'scan-quality':       2,
    'markup':             3,
    'question':           3,
    'content-enhancement':4,
}

# Type assignments
types = {
    'link-target': [24, 172],
    'text-correction': [
        # minor
        5, 43, 58, 106, 107, 108, 109, 110, 123, 124, 128,
        145, 146, 156, 157, 158, 160, 161, 162, 163, 165, 171,
        174, 185, 194, 200,
        # medium
        15, 17, 18, 19, 20, 21, 25, 30, 33, 34, 35, 36, 37,
        39, 40, 41, 42, 47, 48, 49, 50, 51, 52, 53, 56, 57,
        59, 60, 61, 62, 63, 64, 66, 67, 73, 79, 80, 84, 90,
        91, 92, 95, 101, 102, 104, 111, 112, 114, 116, 117,
        118, 121, 125, 127, 130, 132, 135, 140, 141, 142, 143,
        144, 148, 149, 150, 152, 153, 154, 155, 159, 164, 166,
        167, 168, 169, 170, 176, 179, 184, 187, 190, 191, 199,
        202, 204, 205, 206, 208, 209, 210, 211, 212, 214, 216,
        217, 218, 220,
    ],
    'encoding': [12, 22, 29, 38, 45, 65, 71, 72, 75, 77, 177, 178, 188],
    'bug': [3, 4, 6, 8, 9, 55, 82, 83, 89, 94, 129, 136, 137,
            139, 182, 186, 189, 192, 193, 197, 213, 215],
    'scan-quality': [54],
    'markup': [10, 13, 44, 74, 78, 113, 120, 147, 175, 181, 183, 196],
    'question': [
        1, 2, 7, 11, 14, 16, 23, 27, 31, 32, 46, 68, 69, 70,
        76, 81, 85, 87, 88, 93, 96, 97, 98, 99, 100, 103, 105,
        115, 119, 122, 126, 133, 134, 138, 151, 173, 180, 198,
        203, 207,
    ],
    'content-enhancement': [26, 28, 86, 131, 195, 201, 219],
}

# Severity overrides — default is minor; these get medium
medium_nums = set([
    # link-target
    172,
    # text-correction medium batch/daily issues
    15, 17, 18, 19, 20, 21, 25, 30, 33, 34, 35, 36, 37,
    39, 40, 41, 42, 47, 48, 49, 50, 51, 52, 53, 56, 57,
    59, 60, 61, 62, 63, 64, 66, 67, 73, 79, 80, 84, 90,
    91, 92, 95, 101, 102, 104, 111, 112, 114, 116, 117,
    118, 121, 125, 127, 130, 132, 135, 140, 141, 142, 143,
    144, 148, 149, 150, 152, 153, 154, 155, 159, 164, 166,
    167, 168, 169, 170, 176, 179, 184, 187, 190, 191, 199,
    202, 204, 205, 206, 208, 209, 210, 211, 212, 214, 216,
    217, 218, 220,
    # encoding medium
    29, 45,
    # markup medium
    13, 183,
    # content-enhancement medium
    195, 219,
])

# Stale bug/question labels to delete after type assignment
# key = issue number, value = label to delete
stale_deletes = {
    33: 'bug', 34: 'bug', 35: 'bug', 36: 'bug', 37: 'bug',
    38: 'bug', 40: 'bug', 54: 'bug', 71: 'bug', 90: 'bug',
    181: 'bug', 188: 'bug', 29: 'bug',
    45: 'question',
}

# Validate total
total = sum(len(v) for v in types.values())
all_nums = set(n for v in types.values() for n in v)
assert total == len(all_nums) == 220, f"Expected 220 unique issues, got {total} total / {len(all_nums)} unique"

errors = []
done = 0

for t, nums in types.items():
    ms = ms_map[t]
    for n in nums:
        sev = 'medium' if n in medium_nums else 'minor'

        # Apply type label
        r = subprocess.run(
            ['gh', 'api', f'repos/{ORG}/{REPO}/issues/{n}/labels',
             '-X', 'POST', '-f', f'labels[]={t}'],
            capture_output=True, encoding='utf-8')
        if r.returncode != 0 and '422' not in r.stderr:
            errors.append(f'type {t} #{n}: {r.stderr[:80]}')

        # Apply severity label
        r = subprocess.run(
            ['gh', 'api', f'repos/{ORG}/{REPO}/issues/{n}/labels',
             '-X', 'POST', '-f', f'labels[]={sev}'],
            capture_output=True, encoding='utf-8')
        if r.returncode != 0 and '422' not in r.stderr:
            errors.append(f'sev {sev} #{n}: {r.stderr[:80]}')

        # Set milestone
        r = subprocess.run(
            ['gh', 'api', f'repos/{ORG}/{REPO}/issues/{n}',
             '-X', 'PATCH', '-f', f'milestone={ms}'],
            capture_output=True, encoding='utf-8')
        if r.returncode != 0:
            errors.append(f'milestone #{n}: {r.stderr[:80]}')

        # Delete stale label if needed
        if n in stale_deletes:
            stale = stale_deletes[n]
            r = subprocess.run(
                ['gh', 'api', f'repos/{ORG}/{REPO}/issues/{n}/labels/{stale}',
                 '-X', 'DELETE'],
                capture_output=True, encoding='utf-8')
            if r.returncode != 0 and '404' not in r.stderr:
                errors.append(f'delete {stale} #{n}: {r.stderr[:80]}')

        done += 1
        print(f'{done}/{total} #{n} {t}/{sev}/ms{ms}', flush=True)

if not errors:
    print('DONE no errors.')
else:
    print(f'ERRORS ({len(errors)}):')
    for e in errors:
        print(' ', e)
