import os
import transcoder

def convert_as_roman(infile, outfile):
    """
    Converts 'as' encoding to 'roman' encoding using transcoder.py
    and the as_roman.xml mapping file.
    """
    # Set the directory where as_roman.xml is located
    transcoder_dir = os.path.join(os.path.dirname(__file__), 'transcoder')
    transcoder.transcoder_set_dir(transcoder_dir)
    
    if not os.path.exists(infile):
        print(f"Error: Input file {infile} not found.")
        return

    with open(infile, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    for line in lines:
        # The transcoder uses the mapping in as_roman.xml
        new_line = transcoder.transcoder_processString(line, 'as', 'roman')
        new_lines.append(new_line)
        
    with open(outfile, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    # Paths relative to this script's directory
    pwd = os.path.dirname(__file__)
    infile = os.path.join(pwd, "../../dictionaries/inm/inm_printchange.txt")
    # Using a different output filename to avoid overwriting the source immediately
    outfile = os.path.join(pwd, "../../dictionaries/inm/inm_printchange_roman.txt")
    
    print(f"Converting {infile} to {outfile}...")
    convert_as_roman(infile, outfile)
    print("Conversion complete.")
