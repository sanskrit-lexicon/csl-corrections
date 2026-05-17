import re
import os
import sys

# Tag pattern that matches {{...}}, [[...]], and <chg>...</chg> (including gra-style)
TAG_PATTERN = re.compile(
    r'\{\{.*?\}\}|\[\[.*?\]\]|<chg(?:\s[^>]*)?>(?:(?!</chg>).)*</chg>',
    re.DOTALL
)


def is_matching_tag(tag_text, old_val, new_val):
    """Return True if the tag represents the OLD->NEW correction."""
    target = f"{old_val}->{new_val}"
    if tag_text.startswith('{{') or tag_text.startswith('[['):
        inner = tag_text[2:-2]
        content = inner.split('||')[0] if '||' in inner else inner
        return content == target
    elif tag_text.startswith('<chg'):
        # gra-style: <chg ...><old>OLD</old><new>NEW</new></chg>
        gra_m = re.match(r'<chg[^>]*><old>(.*?)</old><new>(.*?)</new></chg>',
                         tag_text, re.DOTALL)
        if gra_m:
            return gra_m.group(1) == old_val and gra_m.group(2) == new_val
        # simple: <chg ...>OLD->NEW</chg>
        simple_m = re.match(r'<chg[^>]*>(.*?)</chg>', tag_text, re.DOTALL)
        if simple_m:
            return simple_m.group(1) == target
    return False


def merge_metadata(existing_tag, change_data):
    """
    Fill missing metadata fields in an existing correction tag.
    Returns (updated_tag_text, was_updated).

    Handles:
    1. {{OLD->NEW}} or {{OLD->NEW||DATE|USER|REF|COMMENT}}  (also [[...]])
    2. <chg ...>OLD->NEW</chg>                              (simple format)
    3. <chg ...><old>OLD</old><new>NEW</new></chg>          (gra-style)
    """
    old_val = change_data['old']
    new_val = change_data['new']
    target = f"{old_val}->{new_val}"
    updated = False

    # --- Format 1/2: {{...}} or [[...]] ---
    if (existing_tag.startswith('{{') and existing_tag.endswith('}}')) or \
       (existing_tag.startswith('[[') and existing_tag.endswith(']]')):
        dopen, dclose = existing_tag[:2], existing_tag[-2:]
        inner = existing_tag[2:-2]
        if '||' in inner:
            content, meta_str = inner.split('||', 1)
            parts = meta_str.split('|')
        else:
            content, parts = inner, []
        if content != target:
            return existing_tag, False
        while len(parts) < 4:
            parts.append('')
        nm = list(parts)
        if not nm[0] and change_data.get('date'):
            nm[0] = change_data['date'];   updated = True
        if not nm[1] and change_data.get('source'):
            nm[1] = change_data['source']; updated = True
        if not nm[2] and change_data.get('ref'):
            nm[2] = change_data['ref'];    updated = True
        if not nm[3] and change_data.get('comment'):
            nm[3] = change_data['comment']; updated = True
        if updated:
            return f"{dopen}{content}||{'|'.join(nm)}{dclose}", True
        return existing_tag, False

    # --- Format 3/4: <chg ...>...</chg> ---
    elif existing_tag.startswith('<chg'):
        # Try gra-style first
        gra_m = re.match(
            r'<chg(?P<attrs>[^>]*)><old>(?P<ov>.*?)</old><new>(?P<nv>.*?)</new></chg>',
            existing_tag, re.DOTALL)
        if gra_m:
            if gra_m.group('ov') != old_val or gra_m.group('nv') != new_val:
                return existing_tag, False
            attrs_str = gra_m.group('attrs')
            existing_attr_keys = set(re.findall(r'(\w+)="[^"]*"', attrs_str))
            additions = []
            for key, field in [('date','date'), ('user','source'),
                                ('href','ref'), ('note','comment')]:
                if key not in existing_attr_keys and change_data.get(field):
                    additions.append(f'{key}="{change_data[field]}"')
                    updated = True
            if updated:
                suffix = (' ' + ' '.join(additions)) if additions else ''
                return (f'<chg{attrs_str}{suffix}>'
                        f'<old>{old_val}</old><new>{new_val}</new></chg>'), True
            return existing_tag, False

        # Try simple format
        simple_m = re.match(r'<chg(?P<attrs>.*?)>(?P<content>.*?)</chg>',
                             existing_tag, re.DOTALL)
        if simple_m:
            content = simple_m.group('content')
            if content != target:
                return existing_tag, False
            attrs_str = simple_m.group('attrs')
            attrs = dict(re.findall(r'(\w+)="([^"]*)"', attrs_str))
            for key, field in [('date','date'), ('user','source'),
                                ('href','ref'), ('note','comment')]:
                if not attrs.get(key) and change_data.get(field):
                    attrs[key] = change_data[field]; updated = True
            if updated:
                ordered = ['date', 'user', 'href', 'note']
                fa = [f'{k}="{attrs[k]}"' for k in ordered if attrs.get(k)]
                fa += [f'{k}="{v}"' for k, v in attrs.items()
                       if k not in ordered and v]
                new_attrs = (' ' + ' '.join(fa)) if fa else ''
                return f'<chg{new_attrs}>{content}</chg>', True
            return existing_tag, False

    return existing_tag, False


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 issue87.py <dict_code> [change_file_path]")
        sys.exit(1)

    dict_code = sys.argv[1]
    if len(sys.argv) > 2:
        change_file = sys.argv[2]
    else:
        change_file = os.path.join('..', '..', 'dictionaries', dict_code,
                                   f'{dict_code}_printchange.txt')

    orig_file = os.path.join('..', '..', '..', 'csl-orig', 'v02',
                             dict_code, f'{dict_code}.txt')
    output_file = f'temp_{dict_code}.txt'

    YELLOW = '\033[93m'
    RESET  = '\033[0m'

    if not os.path.exists(change_file):
        print(f"Error: Change file {change_file} not found.")
        sys.exit(1)
    if not os.path.exists(orig_file):
        print(f"Error: Original file {orig_file} not found.")
        sys.exit(1)

    # Determine tag type for new replacements
    basename = os.path.basename(change_file)
    start_tag, end_tag = ('{{', '}}') if 'printchange' in basename else ('[[', ']]')

    # --- Parse printchange file ---
    changes = []
    with open(change_file, 'r', encoding='utf-8') as f:
        content_pc = f.read()

    blocks = re.split(r'-{10,}', content_pc)
    for block in blocks:
        lines = block.split('\n')
        date = source = ref = ''
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            date_match = re.search(r'(\d{2})[/-](\d{2})[/-](\d{4})', stripped)
            if date_match and not date:
                m, d, y = date_match.groups()
                date = f"{y}{m}{d}"
                if len(stripped) < 15:
                    continue
            if stripped.lower().startswith('source:'):
                source = stripped[7:].strip(); continue
            if stripped.lower().startswith('ref:'):
                ref = stripped[4:].strip(); continue
            if 'reference' in stripped.lower() and 'http' in stripped:
                url_m = re.search(r'(https?://\S+)', stripped)
                if url_m:
                    ref = url_m.group(1); continue
            if stripped.startswith('L code'):
                continue
            num_cols = stripped.count(':') - stripped.count(':/')
            if stripped[0:1].isdigit() and num_cols in [3, 4]:
                parts = [p.strip() for p in stripped.split(':')]
                if 4 <= len(parts) <= 5:
                    comment = parts[4] if len(parts) == 5 else ''
                    changes.append({
                        'lcode': parts[0], 'headword': parts[1],
                        'old': parts[2],   'new': parts[3],
                        'date': date,      'source': source,
                        'ref': ref,        'comment': comment,
                        'found_any': False
                    })

    # --- Read and index original file ---
    with open(orig_file, 'r', encoding='utf-8') as f:
        content = f.read()

    entry_regex = re.compile(r'(<L>([^<]+).*?<k1>([^<]+)[\s\S]*?<LEND>)')
    all_entries = list(entry_regex.finditer(content))

    lcode_to_indices = {}
    hw_to_indices = {}
    for i, match in enumerate(all_entries):
        lcode = re.split(r'[<]', match.group(2).strip())[0].strip()
        hw = match.group(3).strip()
        lcode_to_indices.setdefault(lcode, []).append(i)
        hw_to_indices.setdefault(hw, []).append(i)

    modified_sections = {i: all_entries[i].group(0).split('\n')
                         for i in range(len(all_entries))}

    # --- Core replacement function ---
    def try_replace(target_indices, change_data, requested_lcode, is_fallback=False):
        newly_tagged_total  = 0
        already_tagged_total = 0
        new_val = change_data['new']
        old_val = change_data['old']
        hw_val  = change_data['headword']

        for idx in target_indices:
            block_lines = modified_sections[idx]
            total_count  = 0
            already_count = 0
            used_val = '(unknown)'

            new_block_lines = []
            for line in block_lines:
                if line.startswith('<L>'):
                    new_block_lines.append(line)
                    continue

                # Find all existing tags ({{...}}, [[...]], <chg>)
                line_tags = list(TAG_PATTERN.finditer(line))

                # --- Step 1: merge missing metadata into any matching existing tag ---
                updated_line = line
                meta_merged = 0
                for t in reversed(line_tags):
                    new_tag_text, was_updated = merge_metadata(t.group(0), change_data)
                    if was_updated:
                        updated_line = (updated_line[:t.start()]
                                        + new_tag_text
                                        + updated_line[t.end():])
                        meta_merged += 1

                if meta_merged:
                    line = updated_line
                    total_count += meta_merged
                    used_val = f"{old_val}->{new_val} (metadata updated)"
                    # Recalculate tags after update
                    line_tags = list(TAG_PATTERN.finditer(line))

                # --- Step 2: count tags that already have this correction (no update needed) ---
                for t in line_tags:
                    tag_text = t.group(0)
                    if is_matching_tag(tag_text, old_val, new_val):
                        # Only count as 'already done' if merge_metadata didn't touch it
                        # (i.e., all metadata was already present)
                        _, would_update = merge_metadata(tag_text, change_data)
                        if not would_update:
                            already_count += 1

                # --- Step 3: normal search-and-replace for untagged occurrences ---
                if not meta_merged:
                    search_vals = []
                    if new_val:
                        search_vals.append(new_val)
                    if old_val and old_val != new_val:
                        search_vals.append(old_val)

                    matches = []
                    line_used_val = None
                    for s_val in search_vals:
                        cur_matches = []
                        if s_val in line:
                            cur_matches = list(re.finditer(re.escape(s_val), line))
                        elif sum(1 for c in s_val if not c.isspace()) >= 2:
                            sep = r'(?:[-\s¦]|\{.*?\})*'
                            rstr = sep.join(re.escape(c) for c in s_val
                                            if not c.isspace())
                            try:
                                cur_matches = list(re.finditer(rstr, line))
                            except re.error:
                                cur_matches = []
                        if cur_matches:
                            # Idempotency: skip matches inside existing tags
                            filtered = [m for m in cur_matches
                                        if not any(t.start() <= m.start()
                                                   and m.end() <= t.end()
                                                   for t in line_tags)]
                            if filtered:
                                matches = filtered
                                line_used_val = s_val
                                break

                    if matches:
                        used_val = line_used_val
                        total_count += len(matches)
                        if start_tag == '{{':
                            meta = (f"{change_data.get('date','')}"
                                    f"|{change_data.get('source','')}"
                                    f"|{change_data.get('ref','')}"
                                    f"|{change_data.get('comment','')}")
                            tag_content = f"{old_val}->{new_val}||{meta}"
                        else:
                            tag_content = f"{old_val}->{new_val}"
                        replacement_tag = f"{start_tag}{tag_content}{end_tag}"
                        for m in reversed(matches):
                            line = line[:m.start()] + replacement_tag + line[m.end():]

                new_block_lines.append(line)

            if total_count > 0:
                if is_fallback:
                    msg = (f"No match in Lcode {requested_lcode} - via Headword"
                           f" {hw_val} - Tagged {total_count} occurrence(s) of '{used_val}'.")
                else:
                    msg = f"{requested_lcode} - Tagged {total_count} occurrence(s) of '{used_val}'."
                if total_count > 1:
                    print(f"{YELLOW}WARNING: {msg}{RESET}")
                else:
                    print(f"INFO: {msg}")
                modified_sections[idx] = new_block_lines

            newly_tagged_total  += total_count
            already_tagged_total += already_count

        return newly_tagged_total, already_tagged_total

    # --- Process each change ---
    for change in changes:
        lcode = change['lcode']
        hw    = change['headword']

        found_by_lcode = False
        if lcode in lcode_to_indices:
            newly, already = try_replace(lcode_to_indices[lcode], change,
                                         lcode, is_fallback=False)
            if newly > 0:
                change['found_any'] = True
                found_by_lcode = True
            elif already > 0:
                change['found_any'] = True
                found_by_lcode = True
                print(f"INFO: {lcode} - correction already fully incorporated in {dict_code}.txt")

        if not found_by_lcode:
            if hw in hw_to_indices:
                indices = hw_to_indices[hw]
                if len(indices) == 1:
                    newly, already = try_replace(indices, change, lcode, is_fallback=True)
                    if newly > 0:
                        change['found_any'] = True
                    elif already > 0:
                        change['found_any'] = True
                        print(f"INFO: {lcode} - correction already fully incorporated in {dict_code}.txt")
                    else:
                        print(f"{YELLOW}WARNING: {lcode} - Headword '{hw}' found"
                              f" but neither old nor new value found in its block{RESET}")
                else:
                    print(f"{YELLOW}WARNING: {lcode} - Headword '{hw}' has"
                          f" {len(indices)} matches, cannot fallback{RESET}")
            else:
                if lcode in lcode_to_indices:
                    print(f"{YELLOW}WARNING: {lcode} - neither old nor new value found in block{RESET}")
                else:
                    print(f"{YELLOW}WARNING: {lcode} - L number not found AND"
                          f" Headword '{hw}' not found in {orig_file}{RESET}")

    applied = sum(1 for c in changes if c['found_any'])
    print(f"Applied {applied} / {len(changes)} changes.")

    # --- Reconstruct output file ---
    parts = []
    last_end = 0
    for i, match in enumerate(all_entries):
        parts.append(content[last_end:match.start()])
        parts.append('\n'.join(modified_sections[i]))
        last_end = match.end()
    parts.append(content[last_end:])

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(''.join(parts))
    print(f"Output written to {output_file}")


if __name__ == "__main__":
    main()
