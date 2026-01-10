import re
from tqdm import tqdm

# ================= SETTINGS =================
INPUT_FILE = "val_clean_30k.txt"       # Your current subset file
OUTPUT_FILE = "val_clean_30k_v2.txt"   # The final clean file
# ============================================

def clean_dataset_precise():
    print(f"🧹 Precise Cleaning of {INPUT_FILE}...")

    # 1. HEADER PATTERN (The Garbage at the Start)
    # Logic: Find "ustar", follow it by any characters, until we hit the zeros.
    # We replace everything matched by this regex with an empty string.
    # We use '0{10,}' to match 10 or more zeros, just to be safe.
    START_GARBAGE = re.compile(r'^.*?ustar.*?0{10,}', re.DOTALL)

    # 2. FOOTER PATTERN (The Filename at the End)
    # Matches: 7 digits - 32 hex chars (the filename of the NEXT doc)
    END_GARBAGE = re.compile(r'\d{7}-[a-f0-9]{32}\s*$')

    cleaned_count = 0
    
    with open(INPUT_FILE, "r", encoding="utf-8", errors="ignore") as fin:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
            
            for line in tqdm(fin):
                cleaned_line = line

                # --- STEP 1: Remove Header using your observation ---
                if "ustar" in cleaned_line:
                    # Replace everything from start up to '00000000000000' with nothing
                    cleaned_line = START_GARBAGE.sub('', cleaned_line)
                
                # --- STEP 2: Remove Footer (Filename) ---
                # Remove the ID at the end (e.g. 0999204-f29...)
                cleaned_line = END_GARBAGE.sub('', cleaned_line)

                # --- STEP 3: Final Polish ---
                # Remove leading/trailing spaces and potential null bytes
                cleaned_line = cleaned_line.strip().replace('\x00', '')

                # # Only save if there is actual text left
                # if len(cleaned_line) > 20: 
                fout.write(cleaned_line + "\n")
                cleaned_count += 1

    print(f"✅ Done! Cleaned text saved to: {OUTPUT_FILE}")
    print(f"📊 Documents saved: {cleaned_count}")

if __name__ == "__main__":
    clean_dataset_precise()