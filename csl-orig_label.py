import subprocess, json, sys, re, time
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ORG = 'sanskrit-lexicon'
REPO = 'csl-orig'

MS = {
    'link-target':         4,
    'link-splitting':      4,
    'text-correction':     5,
    'encoding':            5,
    'bug':                 5,
    'scan-quality':        5,
    'markup':              6,
    'question':            6,
    'content-enhancement': 7,
}

DEFAULT_SEV = {
    'link-target':         'medium',
    'link-splitting':      'medium',
    'markup':              'minor',
    'text-correction':     'minor',
    'content-enhancement': 'medium',
    'encoding':            'minor',
    'bug':                 'minor',
    'scan-quality':        'minor',
    'question':            'minor',
}

HARD = {450, 2797, 1773, 1641}
MEDIUM = {2827, 1615, 630, 628, 627, 626, 629, 468,
          2817, 1786, 1060, 526, 315, 1782, 853, 318}

TYPE_LABELS = {'link-target','link-splitting','markup','text-correction',
               'content-enhancement','encoding','scan-quality','bug','question'}
SEV_LABELS = {'minor','medium','hard'}

DICT_LINENUM = re.compile(r'^[a-z0-9]+:\d+[\d.]*\s*$', re.I)

def classify_type(n, title, labels):
    lblset = set(labels)
    t = title.lower().strip()
    for tp in ['link-target','link-splitting','content-enhancement','markup',
               'text-correction','encoding','bug','scan-quality','question']:
        if tp in lblset:
            return tp
    if 'print change' in lblset:
        return 'text-correction'
    if 'OCR' in lblset:
        return 'scan-quality'
    if 'enhancement' in lblset:
        return 'content-enhancement'
    if 'bug' in lblset:
        return 'bug'
    if 'question' in lblset:
        return 'question'
    if 'pattern' in lblset or 'scale' in lblset:
        return 'markup'
    if 'doc' in lblset:
        return 'question'
    if lblset & {'miss', 'help wanted', 'good first issue', 'duplicate'}:
        return 'text-correction'
    if DICT_LINENUM.match(title.strip()):
        return 'text-correction'
    if re.search(r'link error|rv link|av link|reference error|errors in.*commit|regenerat.*issue', t):
        return 'bug'
    if re.search(r'\biast\b|candrabindu|hyphenation|diacritic|unicode|->.*[ā-ṻ]|śesha|encoding', t):
        return 'encoding'
    if re.search(r'image in text|\bimage\b', t):
        return 'scan-quality'
    if re.search(r'\bmarkup\b|abbreviat|upasarga|headword.*format|separating|separator|malformed|expand.*`|add.*markup|add.*ls|missing.*abbrev', t):
        return 'markup'
    return 'text-correction'

def classify_sev(n, issue_type):
    if n in HARD:
        return 'hard'
    if n in MEDIUM:
        return 'medium'
    return DEFAULT_SEV[issue_type]

def api_call(args, retry=True):
    r = subprocess.run(['gh', 'api'] + args, capture_output=True, encoding='utf-8')
    if r.returncode != 0 and ('rate limit' in r.stderr.lower() or '403' in r.stderr):
        if retry:
            print('Rate limited — sleeping 65s...', flush=True)
            time.sleep(65)
            r = subprocess.run(['gh', 'api'] + args, capture_output=True, encoding='utf-8')
    return r

# Fetch all issues with current label+milestone state
print('Fetching all issues...', flush=True)
issues = []
page = 1
while True:
    r = api_call([f'repos/{ORG}/{REPO}/issues?state=all&per_page=100&page={page}',
                  '--jq', '[.[] | {n:.number, title:.title, labels:[.labels[].name], ms:.milestone.number}]'])
    if r.returncode != 0 or not r.stdout.strip():
        break
    batch = json.loads(r.stdout)
    if not batch:
        break
    issues.extend(batch)
    page += 1
    if page % 5 == 0:
        print(f'  fetched {len(issues)}...', flush=True)

print(f'Total issues: {len(issues)}', flush=True)

# Classify and skip already-done
assignments = []
skipped = 0
type_counts = {}
for iss in issues:
    n = iss['n']
    lblset = set(iss['labels'])
    has_type = bool(lblset & TYPE_LABELS)
    has_sev  = bool(lblset & SEV_LABELS)
    has_ms   = iss['ms'] is not None
    if has_type and has_sev and has_ms:
        skipped += 1
        continue
    tp = classify_type(n, iss['title'], iss['labels'])
    sev = classify_sev(n, tp)
    ms = MS[tp]
    stale = []
    if 'bug' in lblset and tp != 'bug':
        stale.append('bug')
    if 'question' in lblset and tp != 'question':
        stale.append('question')
    assignments.append((n, tp, sev, ms, stale))
    type_counts[tp] = type_counts.get(tp, 0) + 1

print(f'Skipped (already done): {skipped}')
print(f'To process: {len(assignments)}')
print('Type distribution (remaining):')
for tp, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f'  {tp}: {cnt}')

# Apply labels
errors = []
done = 0
total = len(assignments)

for n, tp, sev, ms, stale in assignments:
    # POST both labels at once
    r = api_call([f'repos/{ORG}/{REPO}/issues/{n}/labels',
                  '-X', 'POST', '-f', f'labels[]={tp}', '-f', f'labels[]={sev}'])
    if r.returncode != 0 and '422' not in r.stderr:
        errors.append(f'labels #{n}: {r.stderr[:80]}')

    # PATCH milestone
    r = api_call([f'repos/{ORG}/{REPO}/issues/{n}',
                  '-X', 'PATCH', '-f', f'milestone={ms}'])
    if r.returncode != 0:
        errors.append(f'milestone #{n}: {r.stderr[:80]}')

    # Delete stale labels
    for stale_lbl in stale:
        r = api_call([f'repos/{ORG}/{REPO}/issues/{n}/labels/{stale_lbl}', '-X', 'DELETE'])
        if r.returncode != 0 and '404' not in r.stderr:
            errors.append(f'del {stale_lbl} #{n}: {r.stderr[:80]}')

    done += 1
    if done % 100 == 0:
        print(f'{done}/{total} done', flush=True)

print(f'{done}/{total} done')
if not errors:
    print('DONE no errors.')
else:
    print(f'ERRORS ({len(errors)}):')
    for e in errors[:30]:
        print(' ', e)
