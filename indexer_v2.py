# This script only scans the file to find the byte positions of every .txt occurrence. 
# It saves these positions to a lightweight .pkl file.

import mmap
import re
import pickle
import os
from tqdm import tqdm

# ================= SETTINGS =================
INPUT_FILE = "val_split.txt"             # Your large dataset
INDEX_FILE = "val_txt_separators.pkl"    # The output index file
# ============================================

def create_index():
    print(f"🕵️ Scanning {INPUT_FILE} for '.txt' markers...")
    
    # We look for the literal bytes ".txt"
    # This acts as the separator between documents.
    separator_pattern = re.compile(b'\.txt')
    
    # We will store tuples: (start_byte, end_byte) of every ".txt" found
    separator_positions = []
    
    try:
        with open(INPUT_FILE, "r+b") as f:
            # Memory map the file to scan 45GB efficiently without RAM issues
            with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                
                print("⏳ Indexing... (this will take a few minutes)")
                
                # finditer yields match objects. We store the start/end of the match.
                for match in tqdm(separator_pattern.finditer(mm)):
                    separator_positions.append((match.start(), match.end()))
                
    except FileNotFoundError:
        print(f"❌ Error: File {INPUT_FILE} not found.")
        return

    count = len(separator_positions)
    print(f"\n✅ Indexing complete.")
    print(f"📊 Found {count} '.txt' separators.")
    
    # If we have N separators, we can create N-1 documents between them.
    if count < 2:
        print("⚠️ Warning: Fewer than 2 separators found. Cannot define 'between' intervals.")
    
    print(f"💾 Saving index to {INDEX_FILE}...")
    with open(INDEX_FILE, "wb") as f:
        pickle.dump(separator_positions, f)

if __name__ == "__main__":
    create_index()