import re
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 issue87.py <dict_code> [change_file_path]")
        sys.exit(1)
        
    dict_code = sys.argv[1]
    if len(sys.argv) > 2:
        change_file = sys.argv[2]
    else:
        change_file = os.path.join('..', '..', 'dictionaries', dict_code, f'{dict_code}_printchange.txt')
        
    orig_file = os.path.join('..', '..', '..', 'csl-orig', 'v02', dict_code, f'{dict_code}.txt')
    output_file = f'temp_{dict_code}.txt'
    
    # ANSI escape codes for coloring
    YELLOW = '\033[93m'
    RESET = '\033[0m'
    
    # Check if files exist
    if not os.path.exists(change_file):
        print(f"Error: Change file {change_file} not found.")
        sys.exit(1)
    if not os.path.exists(orig_file):
        print(f"Error: Original file {orig_file} not found.")
        sys.exit(1)

    # Determine tag type
    basename = os.path.basename(change_file)
    if 'printchange' in basename:
        start_tag, end_tag = '{{', '}}'
    else:
        start_tag, end_tag = '[[', ']]'

    # Read changes
    changes = []
    with open(change_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            stripped = line.strip()
            if not stripped:
                continue
                
            num_cols = stripped.count(':') - stripped.count(':/')
            
            if stripped[0].isdigit() and num_cols in [3, 4]:
                parts = [p.strip() for p in stripped.split(':')]
                if 4 <= len(parts) <= 5:
                    changes.append({
                        'lcode': parts[0],
                        'headword': parts[1],
                        'old': parts[2],
                        'new': parts[3],
                        'found_any': False
                    })
            elif num_cols > 0:
                if not stripped.startswith(('Source:', 'Ref:', 'L code :')):
                    has_non_ascii = any(ord(c) > 127 for c in stripped)
                    if has_non_ascii or stripped[0].isdigit():
                        print(f"{YELLOW}WARNING: Malformed line at {line_num} - {stripped}{RESET}")

    # Read original file
    with open(orig_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into entries
    entry_regex = re.compile(r'(<L>([^<]+).*?<k1>([^<]+)[\s\S]*?<LEND>)')
    all_entries = list(entry_regex.finditer(content))
    
    # Map Lcode and Headword to indices
    lcode_to_indices = {}
    hw_to_indices = {}
    
    for i, match in enumerate(all_entries):
        lcode_raw = match.group(2).strip()
        lcode = re.split(r'[<]', lcode_raw)[0].strip()
        
        hw = match.group(3).strip()
        
        if lcode not in lcode_to_indices:
            lcode_to_indices[lcode] = []
        lcode_to_indices[lcode].append(i)
        
        if hw not in hw_to_indices:
            hw_to_indices[hw] = []
        hw_to_indices[hw].append(i)

    # modified_sections initialized with original content (split into lines)
    modified_sections = {i: all_entries[i].group(0).split('\n') for i in range(len(all_entries))}
    
    def try_replace(target_indices, change_data, requested_lcode, is_fallback=False):
        found_any = False
        new_val = change_data['new']
        old_val = change_data['old']
        hw_val = change_data['headword']
        
        for idx in target_indices:
            block_lines = modified_sections[idx]
            total_count = 0
            used_val = '(unknown)'
            
            new_block_lines = []
            for line in block_lines:
                if line.startswith('<L>'):
                    new_block_lines.append(line)
                    continue
                
                matches = []
                search_vals = []
                if new_val:
                    search_vals.append(new_val)
                if old_val and old_val != new_val:
                    search_vals.append(old_val)
                
                line_used_val = None
                for s_val in search_vals:
                    if s_val in line:
                        pattern = re.escape(s_val)
                        matches = list(re.finditer(pattern, line))
                    elif sum(1 for c in s_val if not c.isspace()) >= 2:
                        sep_pattern = r'(?:[-\s¦]|{.*?}|<.*?>)*'
                        regex_str = sep_pattern.join([re.escape(c) for c in s_val if not c.isspace()])
                        try:
                            matches = list(re.finditer(regex_str, line))
                        except re.error:
                            matches = []
                    
                    if matches:
                        line_used_val = s_val
                        break
                
                if matches:
                    used_val = line_used_val
                    total_count += len(matches)
                    
                    tag_content = f"{old_val}->{new_val}"
                    replacement_tag = f"{start_tag}{tag_content}{end_tag}"
                    
                    for m in reversed(matches):
                        line = line[:m.start()] + replacement_tag + line[m.end():]
                
                new_block_lines.append(line)
            
            if total_count > 0:
                found_any = True
                
                if is_fallback:
                    msg_body = f"No match found in Lcode {requested_lcode} - Searched via Headword - {hw_val} - Tagged {total_count} occurrence(s) of '{used_val}'."
                else:
                    msg_body = f"{requested_lcode} - Tagged {total_count} occurrence(s) of '{used_val}'."
                
                if total_count > 3:
                    print(f"{YELLOW}WARNING: {msg_body}{RESET}")
                else:
                    print(f"INFO: {msg_body}")
                
                modified_sections[idx] = new_block_lines
                
        return found_any

    # Process each change in the order of occurrence in change_file
    for change in changes:
        lcode = change['lcode']
        hw = change['headword']
        
        # 1. Try the provided Lcode
        found_by_lcode = False
        if lcode in lcode_to_indices:
            found_by_lcode = try_replace(lcode_to_indices[lcode], change, lcode, is_fallback=False)
            if found_by_lcode:
                change['found_any'] = True
        
        # 2. Fallback to Headword if Lcode failed
        if not found_by_lcode:
            if hw in hw_to_indices:
                indices = hw_to_indices[hw]
                if len(indices) == 1:
                    found_by_hw = try_replace(indices, change, lcode, is_fallback=True)
                    if found_by_hw:
                        change['found_any'] = True
                    else:
                        print(f"{YELLOW}WARNING: {lcode} - Headword '{hw}' found but neither old nor new value found in its block{RESET}")
                else:
                    print(f"{YELLOW}WARNING: {lcode} - Headword '{hw}' has {len(indices)} matches in dictionary, cannot fallback{RESET}")
            else:
                if lcode in lcode_to_indices:
                    print(f"{YELLOW}WARNING: {lcode} - neither old nor new value found in block{RESET}")
                else:
                    print(f"{YELLOW}WARNING: {lcode} - L number not found AND Headword '{hw}' not found in {orig_file}{RESET}")

    applied = sum(1 for c in changes if c['found_any'])
    print(f"Applied {applied} / {len(changes)} changes.")

    # Reconstruct the file content
    new_content_parts = []
    last_end = 0
    for i, match in enumerate(all_entries):
        new_content_parts.append(content[last_end:match.start()])
        new_content_parts.append('\n'.join(modified_sections[i]))
        last_end = match.end()
    
    new_content_parts.append(content[last_end:])
    final_content = "".join(new_content_parts)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

if __name__ == "__main__":
    main()
