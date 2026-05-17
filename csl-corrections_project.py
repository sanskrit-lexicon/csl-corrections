import subprocess, json, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

ORG = 'sanskrit-lexicon'
REPO = 'csl-corrections'

# Project node IDs (projects 1-4, for all repos except MWS)
# DTB=1 → PVT_kwDOAGGnOc4BW400
# DQ=2  → PVT_kwDOAGGnOc4BW402
# SD=3  → PVT_kwDOAGGnOc4BW404
# ME=4  → PVT_kwDOAGGnOc4BW405
proj_node = {
    1: 'PVT_kwDOAGGnOc4BW400',
    2: 'PVT_kwDOAGGnOc4BW402',
    3: 'PVT_kwDOAGGnOc4BW404',
    4: 'PVT_kwDOAGGnOc4BW405',
}

# Fetch all issue node IDs with milestone
def fetch_all():
    items = []
    page = 1
    while True:
        r = subprocess.run(
            ['gh', 'api',
             f'repos/{ORG}/{REPO}/issues?state=all&per_page=100&page={page}',
             '--jq', '[.[] | {number:.number, nodeId:.node_id, ms:.milestone.number}]'],
            capture_output=True, encoding='utf-8')
        if r.returncode != 0 or not r.stdout.strip():
            break
        batch = json.loads(r.stdout)
        if not batch:
            break
        items.extend(batch)
        page += 1
    return items

issues = fetch_all()
print(f'Fetched {len(issues)} issues for project assignment')

errors = []
done = 0
total = len(issues)

for iss in issues:
    n = iss['number']
    node_id = iss['nodeId']
    ms = iss['ms']
    if ms is None:
        errors.append(f'#{n} has no milestone — skipping')
        continue
    proj_id = proj_node.get(ms)
    if not proj_id:
        errors.append(f'#{n} milestone {ms} not in proj_node map')
        continue

    mutation = '''mutation($proj:ID!,$item:ID!){
      addProjectV2ItemById(input:{projectId:$proj,contentId:$item}){item{id}}
    }'''
    r = subprocess.run(
        ['gh', 'api', 'graphql',
         '-f', f'query={mutation}',
         '-f', f'proj={proj_id}',
         '-f', f'item={node_id}'],
        capture_output=True, encoding='utf-8')
    if r.returncode != 0:
        resp = r.stdout + r.stderr
        if 'Could not resolve to a node' in resp or 'already exists' in resp.lower():
            errors.append(f'warn #{n}: {resp[:80]}')
        else:
            errors.append(f'ERROR #{n}: {resp[:80]}')
    done += 1
    if done % 20 == 0:
        print(f'{done}/{total} done', flush=True)

print(f'{done}/{total} done')
if not errors:
    print('DONE no errors.')
else:
    print(f'ERRORS/WARNS ({len(errors)}):')
    for e in errors[:20]:
        print(' ', e)
