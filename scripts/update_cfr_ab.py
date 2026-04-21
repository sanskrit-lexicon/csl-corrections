import os
from datetime import datetime

def update_cfr_ab():
    cfr_ab_path = 'cfr_ab/cfr_ab.tsv'
    daily_dir = 'daily'
    start_date = '20260404'
    start_dt = datetime.strptime(start_date, '%Y%m%d')
    output_lines = []
    
    print(f"Updating {cfr_ab_path}...")
    print(f"Daily folder start date: {start_date}")

    # 1. Keep lines before start_date
    if os.path.exists(cfr_ab_path):
        with open(cfr_ab_path, 'r', encoding='utf-8') as f:
            header = f.readline()
            if header:
                output_lines.append(header)
            
            for line in f:
                if not line.strip():
                    continue
                parts = line.split('\t')
                timestamp_str = parts[0].strip()
                try:
                    # Timestamp format: MM/DD/YYYY HH:MM:SS
                    # We only care about the date part for comparison
                    dt = datetime.strptime(timestamp_str[:10], '%m/%d/%Y')
                    if dt < start_dt:
                        output_lines.append(line)
                except (ValueError, IndexError):
                    # If it doesn't match the timestamp format, it's either an older entry with different format
                    # or some other data we want to preserve.
                    output_lines.append(line)
    else:
        # If the file doesn't exist, we start with a header
        output_lines.append('\tWhich Dictionary?\tWhich L code?\tHeadword\tOld \tNew\tComment\tYour Email Address\n')

    print(f"Preserved {len(output_lines)} lines from before {start_date} (including header).")

    # 2. Append data from daily folders
    if not os.path.isdir(daily_dir):
        print(f"Warning: {daily_dir} directory not found.")
    else:
        daily_subdirs = sorted([d for d in os.listdir(daily_dir) if d.isdigit() and len(d) == 8])
        
        for date_str in daily_subdirs:
            if date_str < start_date:
                continue
                
            subdir_p = os.path.join(daily_dir, date_str)
            corrected_file = os.path.join(subdir_p, f'cfr-{date_str}-corrected.tsv')
            normal_file = os.path.join(subdir_p, f'cfr-{date_str}.tsv')
            
            file_to_read = None
            if os.path.exists(corrected_file):
                file_to_read = corrected_file
                # print(f"  Using corrected file for {date_str}")
            elif os.path.exists(normal_file):
                file_to_read = normal_file
                # print(f"  Using normal file for {date_str}")
                
            if file_to_read:
                with open(file_to_read, 'r', encoding='utf-8') as f:
                    added_count = 0
                    for line in f:
                        if line.strip():
                            # The daily files shouldn't have headers, but let's be safe
                            if not line.startswith('\tWhich Dictionary?'):
                                output_lines.append(line)
                                added_count += 1
                    # print(f"  Added {added_count} lines from {date_str}")

    # 3. Deduplicate (preserving order)
    seen = set()
    deduped_lines = []
    for line in output_lines:
        if line not in seen:
            deduped_lines.append(line)
            seen.add(line)
    
    # 4. Sort chronologically
    def get_sort_key(line):
        # Header should always be first
        if line.startswith('\tWhich Dictionary?'):
            return datetime.min
            
        parts = line.split('\t')
        if not parts:
            return datetime.min
        timestamp_str = parts[0].strip()
        try:
            # Full format: MM/DD/YYYY HH:MM:SS
            return datetime.strptime(timestamp_str, '%m/%d/%Y %H:%M:%S')
        except ValueError:
            try:
                # Just date: MM/DD/YYYY
                return datetime.strptime(timestamp_str[:10], '%m/%d/%Y')
            except ValueError:
                # If everything fails, put it at the very beginning (after header)
                # but before valid dates.
                return datetime.min

    # Preserve header, sort the rest
    header = deduped_lines[0]
    data_lines = deduped_lines[1:]
    data_lines.sort(key=get_sort_key)
    final_lines = [header] + data_lines

    print(f"Final line count after deduplication and sorting: {len(final_lines)}")

    # 5. Write back
    os.makedirs(os.path.dirname(cfr_ab_path), exist_ok=True)
    with open(cfr_ab_path, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

if __name__ == "__main__":
    update_cfr_ab()
