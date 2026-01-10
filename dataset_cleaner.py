import re
from tqdm import tqdm

# ================= SETTINGS =================
INPUT_FILE = "val_subset_30k.txt"       # The dirty file you just made
OUTPUT_FILE = "val_clean_30k.txt"       # The final clean file
# ============================================

def clean_dataset():
    print(f"ww Cleaning {INPUT_FILE}...")
    
    # 1. Regex to catch the TAR header
    # Looks for: Numbers -> "ustar" -> Numbers -> End of header
    # matches strings like: "0000644 0000000 ... ustar ... 0000000 "
    TAR_HEADER_PATTERN = re.compile(r'^\s*\d+\s+[\d\s]*ustar\s+[\d\s]+', re.MULTILINE)

    # 2. Regex to clean excessive whitespace (more than 2 newlines becomes 2)
    WHITESPACE_PATTERN = re.compile(r'\n{3,}')
    
    documents_kept = 0
    
    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as fin:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
            
            # We read the file line by line? 
            # CAREFUL: Since your previous script saved docs with just "\n", 
            # we might have trouble knowing where one starts and ends if we read line-by-line.
            # However, usually the TAR header appears at the start of a line.
            
            # Better approach for your specific file format:
            # Read the whole file as a stream (or large chunks) and clean.
            # But to be safe with RAM, let's process line-by-line and assume
            # the "garbage" is usually on the first line of a doc.
            
            for line in tqdm(fin):
                
                # 1. Remove TAR Header if present in this line
                if "ustar" in line:
                    clean_line = TAR_HEADER_PATTERN.sub('', line)
                else:
                    clean_line = line
                
                # 2. Clean Null Bytes
                clean_line = clean_line.replace('\x00', '')
                
                # 3. Trim leading/trailing whitespace of the line
                # (Optional: be careful not to merge words)
                clean_line = clean_line.strip()
                
                # 4. Save if it's not empty
                if len(clean_line) > 0:
                    fout.write(clean_line + "\n")
                    documents_kept += 1

    print(f"✅ Done! Cleaned file saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    clean_dataset()