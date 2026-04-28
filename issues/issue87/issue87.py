import re
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 issue87.py <dict_code>")
        sys.exit(1)
        
    dict_code = sys.argv[1]
    
    # Paths relative to issues/issue87/
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

    # Read changes
    changes = []
    with open(change_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            stripped = line.strip()
            if not stripped:
                continue
                
            num_cols = stripped.count(':')
            
            if stripped[0].isdigit() and num_cols in [3, 4]:
                parts = [p.strip() for p in stripped.split(':')]
                if 4 <= len(parts) <= 5:
                    changes.append({
                        'lcode': parts[0],
                        'old': parts[2],
                        'new': parts[3],
                        'found_lcode': False
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
    entry_regex = re.compile(r'(<L>([^<]+)[\s\S]*?<LEND>)')
    all_entries = list(entry_regex.finditer(content))
    
    # Map Lcode to its index in all_entries
    lcode_to_indices = {}
    for i, match in enumerate(all_entries):
        lcode_raw = match.group(2).strip()
        lcode = re.split(r'[<]', lcode_raw)[0].strip()
        if lcode not in lcode_to_indices:
            lcode_to_indices[lcode] = []
        lcode_to_indices[lcode].append(i)

    # modified_sections initialized with original content
    modified_sections = {i: all_entries[i].group(0) for i in range(len(all_entries))}
    
    # Process each change in the order of occurrence in change_file
    for change in changes:
        lcode = change['lcode']
        old_val = change['old']
        new_val = change['new']
        
        if lcode in lcode_to_indices:
            change['found_lcode'] = True
            indices = lcode_to_indices[lcode]
            found_any_matching = False
            
            for idx in indices:
                block_content = modified_sections[idx]
                
                # We try to match 'new_val' even if there are hyphens or certain separators
                # To handle cases like 'annakozWaka' matching 'anna-kozWaka'
                # We construct a regex that allows optional hyphens or separators between characters
                # Only if the literal 'new_val' is not found
                
                matches = []
                if new_val in block_content:
                    # Literal matches
                    pattern = re.escape(new_val)
                    matches = list(re.finditer(pattern, block_content))
                else:
                    # Hyphen-insensitive and tag-insensitive matching
                    # We allow optional hyphens, spaces, or certain delimiters between letters
                    # This is more robust for 'anna-kozWaka' and '{#azwApada#}¦ {%m.n.%}'
                    
                    # Pattern for each character: char followed by optional separators
                    # Separators: hyphen, space, or common tags like {# #}, {% %}, ¦
                    sep_pattern = r'(?:[-\s¦]|{.*?}|<.*?>)*'
                    regex_str = sep_pattern.join([re.escape(c) for c in new_val if not c.isspace()])
                    
                    # If the original new_val had spaces, we should respect them too
                    # But the sep_pattern already includes \s
                    
                    try:
                        matches = list(re.finditer(regex_str, block_content))
                    except re.error:
                        matches = []
                
                if matches:
                    found_any_matching = True
                    count = len(matches)
                    
                    msg = f"{lcode} - Replaced {count} occurrence(s) of '{new_val}' with choice tag."
                    if count > 3:
                        print(f"{YELLOW}WARNING: {msg}{RESET}")
                    else:
                        print(f"INFO: {msg}")
                    
                    # Apply replacements from end to start to maintain offsets
                    for m in reversed(matches):
                        # found_text = m.group(0)
                        # The user wants New literally in the corr tag
                        replacement = f"<choice><sic>{old_val}</sic><corr>{new_val}</corr></choice>"
                        block_content = block_content[:m.start()] + replacement + block_content[m.end():]
                    
                    modified_sections[idx] = block_content
            
            if not found_any_matching:
                print(f"{YELLOW}WARNING: {lcode} - '{new_val}' not found in block{RESET}")
        else:
            print(f"{YELLOW}WARNING: {lcode} - L number not found in {orig_file}{RESET}")

    # Reconstruct the file content
    new_content_parts = []
    last_end = 0
    for i, match in enumerate(all_entries):
        new_content_parts.append(content[last_end:match.start()])
        new_content_parts.append(modified_sections[i])
        last_end = match.end()
    
    new_content_parts.append(content[last_end:])
    final_content = "".join(new_content_parts)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

if __name__ == "__main__":
    main()
