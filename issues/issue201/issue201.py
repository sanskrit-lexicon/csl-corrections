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

def strip_common_prefix(s1, s2):
    prefix_len = 0
    for c1, c2 in zip(s1, s2):
        if c1 == c2:
            prefix_len += 1
        else:
            break
    return s1[:prefix_len], s1[prefix_len:], s2[prefix_len:]

def strip_common_suffix(s1, s2):
    suffix_len = 0
    for c1, c2 in zip(reversed(s1), reversed(s2)):
        if c1 == c2:
            suffix_len += 1
        else:
            break
    if suffix_len == 0: return s1, s2
    return s1[:-suffix_len], s2[:-suffix_len]

def get_minimal_unique_context(old_val, new_val, before_block, after_block, lines, index):
    # 1. Identify the core difference
    common_pref, core_old_plus, core_new_plus = strip_common_prefix(old_val, new_val)
    core_old, core_new = strip_common_suffix(core_old_plus, core_new_plus)
    common_suff = core_old_plus[len(core_old):]
    
    current_old = core_old
    current_new = core_new
    
    # Check if unique and non-blank in both directions
    def is_safe_unique(old, new):
        if not old.strip() or not new.strip(): return False
        return before_block.count(old) == 1 and after_block.count(new) == 1

    # 2. Expand using chunk context
    pref_idx = len(common_pref) - 1
    suff_idx = 0
    
    while not is_safe_unique(current_old, current_new):
        expanded = False
        if pref_idx >= 0:
            current_old = common_pref[pref_idx] + current_old
            current_new = common_pref[pref_idx] + current_new
            pref_idx -= 1
            expanded = True
            if is_safe_unique(current_old, current_new): break
            
        if suff_idx < len(common_suff):
            current_old = current_old + common_suff[suff_idx]
            current_new = current_new + common_suff[suff_idx]
            suff_idx += 1
            expanded = True
            if is_safe_unique(current_old, current_new): break
            
        if not expanded: break

    # 3. If still not safe/unique, expand using surrounding lines
    if not is_safe_unique(current_old, current_new):
        offset = 1
        while not is_safe_unique(current_old, current_new):
            expanded = False
            # Backwards
            back_idx = index - offset
            if back_idx >= 0:
                line = lines[back_idx]
                mark, chunk = line[0], line[1:]
                for char in reversed(chunk):
                    if mark == ' ':
                        current_old = char + current_old
                        current_new = char + current_new
                    elif mark == '-':
                        current_old = char + current_old
                    elif mark == '+':
                        current_new = char + current_new
                    
                    if is_safe_unique(current_old, current_new): 
                        expanded = True
                        break
                if expanded: break
                expanded = True
            # Forwards
            if not is_safe_unique(current_old, current_new):
                next_start_idx = index
                if lines[index].startswith('-') and index + 1 < len(lines) and lines[index+1].startswith('+'):
                    next_start_idx = index + 1
                
                next_idx = next_start_idx + offset
                if next_idx < len(lines):
                    line = lines[next_idx]
                    mark, chunk = line[0], line[1:]
                    for char in chunk:
                        if mark == ' ':
                            current_old = current_old + char
                            current_new = current_new + char
                        elif mark == '-':
                            current_old = current_old + char
                        elif mark == '+':
                            current_new = current_new + char
                        
                        if is_safe_unique(current_old, current_new):
                            expanded = True
                            break
                    if expanded: break
                    expanded = True
            if not expanded: break
            offset += 1
            if offset > 30: break

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
            
            # Using a very specific word-diff regex to separate tags and words
            word_diff = run_command(['git', 'diff', '--no-index', '--word-diff=porcelain', '--word-diff-regex=[^<>[:space:]]+|<[^>]+>', 'temp_b.txt', 'temp_a.txt'], check=False)
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
                    
                    old_str, new_str = get_minimal_unique_context(deleted, added, before, after, lines, i)
                    
                    # Clean up: replace real newlines with literal \n
                    old_str = old_str.strip().replace('\n', '\\n')
                    new_str = new_str.strip().replace('\n', '\\n')
                    
                    # Ensure we don't have diff artifacts
                    if old_str and not old_str.startswith('--') and not old_str.startswith('++'):
                        changed_entries.append(f"{lcode} : {hw} : {old_str} : {new_str}")
                    
                    if found_added: i += 1
                elif line.startswith('+'):
                    added = line[1:]
                    if not added.strip() or added.startswith('++'):
                        i += 1
                        continue
                    
                    # This is an orphan addition
                    old_str, new_str = get_minimal_unique_context("", added, before, after, lines, i)
                    
                    old_str = old_str.strip().replace('\n', '\\n')
                    new_str = new_str.strip().replace('\n', '\\n')
                    
                    if new_str and not new_str.startswith('++'):
                        changed_entries.append(f"{lcode} : {hw} : {old_str} : {new_str}")
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
