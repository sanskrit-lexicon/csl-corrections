import subprocess, json, sys, time
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ORG  = 'sanskrit-lexicon'
REPO = 'csl-orig'

# org projects 1-4 (non-MWS repos use these)
MS_TO_PROJECT = {
    4: 'PVT_kwDOAGGnOc4BW400',  # DTB
    5: 'PVT_kwDOAGGnOc4BW402',  # DQ
    6: 'PVT_kwDOAGGnOc4BW404',  # SD
    7: 'PVT_kwDOAGGnOc4BW405',  # ME
}

def api(args, retry=True):
    r = subprocess.run(['gh', 'api'] + args, capture_output=True, encoding='utf-8')
    if r.returncode != 0 and ('rate limit' in r.stderr.lower() or '403' in r.stderr):
        if retry:
            print('Rate limited — sleeping 65s...', flush=True)
            time.sleep(65)
            r = subprocess.run(['gh', 'api'] + args, capture_output=True, encoding='utf-8')
    return r

# Fetch all issues with node_id + milestone
print('Fetching issues...', flush=True)
issues = []
page = 1
while True:
    r = api([f'repos/{ORG}/{REPO}/issues?state=all&per_page=100&page={page}',
             '--jq', '[.[] | {number:.number, node_id:.node_id, ms:.milestone.number}]'])
    if r.returncode != 0 or not r.stdout.strip():
        break
    batch = json.loads(r.stdout)
    if not batch:
        break
    issues.extend(batch)
    page += 1
    if page % 5 == 0:
        print(f'  fetched {len(issues)}...', flush=True)

print(f'Total: {len(issues)}', flush=True)

errors = []
done = 0
skipped = 0
total = len(issues)

MUTATION = ('mutation($proj:ID!,$item:ID!){'
            'addProjectV2ItemById(input:{projectId:$proj,contentId:$item})'
            '{item{id}}}')

for iss in issues:
    ms = iss['ms']
    proj = MS_TO_PROJECT.get(ms)
    if proj is None:
        skipped += 1
        continue
    r = api(['graphql', '-f', f'query={MUTATION}',
             '-f', f'proj={proj}', '-f', f'item={iss["node_id"]}'])
    if r.returncode != 0:
        errors.append(f'#{iss["number"]}: {r.stderr[:100]}')
    done += 1
    if done % 200 == 0:
        print(f'{done}/{total} done', flush=True)

print(f'{done}/{total} done ({skipped} skipped, no milestone)')
if not errors:
    print('DONE no errors.')
else:
    print(f'ERRORS ({len(errors)}):')
    for e in errors[:30]:
        print(' ', e)
