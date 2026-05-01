import sys
import subprocess
import re
import datetime
import os

def run_command(args, cwd=None, check=True):
    try:
        return subprocess.check_output(args, cwd=cwd, encoding='utf-8', stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        if not check:
            return e.output
        raise e

def get_blocks(text):
    blocks = []
    # Pattern to match <L>...<LEND>
    pattern = re.compile(r'(<L>([^<]+).*?<LEND>)', re.DOTALL)
    for match in pattern.finditer(text):
        full_block = match.group(1)
        lcode = match.group(2).strip().split('<')[0].split('>')[0].strip()
        blocks.append({'lcode': lcode, 'content': full_block, 'start': match.start(), 'end': match.end()})
    return blocks

def get_headword(block_content):
    match = re.search(r'<k1>([^<]+)', block_content)
    if match:
        return match.group(1)
    return "UNKNOWN"

def get_minimal_unique_context(old_val, new_val, block_content, lines, index):
    # 'lines' is the porcelain word-diff output
    # 'index' is the index of the '-deleted' line
    
    current_old = old_val
    current_new = new_val
    
    # Expand context until unique in block
    offset = 1
    while block_content.count(current_old) > 1:
        expanded = False
        # Try to add word before
        if index - offset >= 0:
            prev_line = lines[index - offset]
            if prev_line.startswith(' '):
                words = prev_line[1:].split()
                if words:
                    context_before = words[-1]
                    current_old = context_before + " " + current_old
                    current_new = context_before + " " + current_new
                    expanded = True
        
        # Try to add word after
        if block_content.count(current_old) > 1:
            # Find next context line
            # The next line could be +added, or a context line
            next_idx = index + (2 if index + 1 < len(lines) and lines[index+1].startswith('+') else 1)
            if next_idx < len(lines):
                next_line = lines[next_idx]
                if next_line.startswith(' '):
                    words = next_line[1:].split()
                    if words:
                        context_after = words[0]
                        current_old = current_old + " " + context_after
                        current_new = current_new + " " + context_after
                        expanded = True
        
        if not expanded:
            break
        offset += 1
        if offset > 10: # Safety break
            break
            
    return current_old, current_new

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 issue201.py <commit_hash> [--dry-run]")
        sys.exit(1)

    commit = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    repo_path = '../../../csl-orig'
    file_rel_path = 'v02/ap/ap.txt'
    target_printchange = '../../dictionaries/ap/ap_printchange.txt'

    # Get the diff for the specific file
    try:
        before_text = run_command(['git', 'show', f'{commit}^:{file_rel_path}'], repo_path)
        after_text = run_command(['git', 'show', f'{commit}:{file_rel_path}'], repo_path)
    except Exception as e:
        print(f"Error reading commit {commit}: {e}")
        sys.exit(1)

    before_blocks = {b['lcode']: b['content'] for b in get_blocks(before_text)}
    after_blocks = {b['lcode']: b['content'] for b in get_blocks(after_text)}

    changed_entries = []
    all_lcodes = sorted(set(before_blocks.keys()) | set(after_blocks.keys()), key=lambda x: float(x) if x.replace('.','',1).isdigit() else 0)

    for lcode in all_lcodes:
        before = before_blocks.get(lcode)
        after = after_blocks.get(lcode)

        if before and after and before != after:
            hw = get_headword(before)
            
            with open('temp_b.txt', 'w') as f: f.write(before)
            with open('temp_a.txt', 'w') as f: f.write(after)
            
            word_diff = run_command(['git', 'diff', '--no-index', '--word-diff=porcelain', 'temp_b.txt', 'temp_a.txt'], check=False)
            os.remove('temp_b.txt')
            os.remove('temp_a.txt')
            
            lines = word_diff.splitlines()
            
            i = 0
            while i < len(lines):
                line = lines[i]
                # Skip diff header lines and chunk separators
                if line.startswith('---') or line.startswith('+++') or line.startswith('@@') or line.startswith('~'):
                    i += 1
                    continue
                    
                if line.startswith('-'):
                    deleted = line[1:]
                    if not deleted.strip() or deleted.startswith('--'): 
                        i += 1
                        continue
                        
                    added = ""
                    found_added = False
                    if i + 1 < len(lines) and lines[i+1].startswith('+'):
                        added = lines[i+1][1:]
                        found_added = True
                    
                    old_str, new_str = get_minimal_unique_context(deleted, added, before, lines, i)
                    
                    # Clean up
                    old_str = old_str.strip().replace('\n', ' ')
                    new_str = new_str.strip().replace('\n', ' ')
                    
                    # Ensure we don't have diff artifacts
                    if old_str and not old_str.startswith('--') and not old_str.startswith('++'):
                        changed_entries.append(f"{lcode} : {hw} : {old_str} : {new_str}")
                    
                    if found_added: i += 1
                i += 1

    if not changed_entries:
        print("No specific word changes identified.")
        return

    # Prepare final output
    date_str = datetime.datetime.now().strftime("%m-%d-%Y")
    commit_url = f"https://github.com/sanskrit-lexicon/csl-orig/commit/{commit}"
    
    output = f"{date_str}\n"
    output += f"Ref: {commit_url}\n"
    output += "L code : Headword : Old  : New : Comment\n"
    for entry in changed_entries:
        output += entry + "\n"
    output += "-----------------------------------------------------------------------\n"

    if dry_run:
        print("DRY RUN: Printing output instead of appending.")
        print(output)
    else:
        with open(target_printchange, 'a') as f:
            f.write(output)
        print(f"Successfully appended {len(changed_entries)} changes to {target_printchange}")

if __name__ == "__main__":
    main()
