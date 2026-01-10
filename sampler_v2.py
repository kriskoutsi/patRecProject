# This script loads the index, picks 𝑁 random intervals between the separators, 
# reads the raw bytes, and saves them. It performs no cleaning.

import pickle
import random
import os
from tqdm import tqdm

# Set random seed for reproducibility
random.seed(42)

# ================= SETTINGS =================
INPUT_FILE = "val_split.txt"        # The large dataset
INDEX_FILE = "val_txt_separators.pkl"     # The index created by the previous script
OUTPUT_FILE = "val_subset_30k.txt" # The final subset
N_DOCUMENTS = 30000                  # Number of random documents
# ============================================

def create_subset():
    if not os.path.exists(INDEX_FILE):
        print(f"❌ Error: {INDEX_FILE} not found. Run indexer.py first.")
        return

    print("📂 Loading index...")
    with open(INDEX_FILE, "rb") as f:
        # These are the positions of the ".txt" markers
        separators = pickle.load(f)
    
    total_separators = len(separators)
    
    # A document is the content strictly BETWEEN two separators.
    # Doc 0 is between separator[0] and separator[1].
    # Total available docs = total_separators - 1
    total_docs = total_separators - 1
    
    if total_docs < 1:
        print("❌ Error: Not enough separators to define documents.")
        return

    print(f"📊 Total available documents: {total_docs}")
    print(f"🎲 Picking {N_DOCUMENTS} random documents...")
    
    # Select random indices
    if N_DOCUMENTS >= total_docs:
        print("⚠️ Requested more documents than available. Taking all.")
        selected_indices = range(total_docs)
    else:
        selected_indices = random.sample(range(total_docs), N_DOCUMENTS)
    
    # Sort indices to read the file sequentially (faster)
    selected_indices.sort()
    
    print(f"📝 Extracting raw data to {OUTPUT_FILE}...")
    
    with open(INPUT_FILE, "rb") as fin:
        with open(OUTPUT_FILE, "w", encoding="utf-8") as fout:
            
            for idx in tqdm(selected_indices):
                # LOGIC:
                # Start reading exactly AFTER the current ".txt" ends
                start_pos = separators[idx][1] 
                
                # Stop reading exactly BEFORE the next ".txt" starts
                end_pos = separators[idx+1][0]
                
                length = end_pos - start_pos
                
                # Edge case: If two .txt are right next to each other
                if length <= 0:
                    continue

                # Go to the position
                fin.seek(start_pos)
                
                # Read raw bytes
                raw_bytes = fin.read(length)
                
                # Decode to string so we can write to a text file.
                # 'errors=ignore' ensures we don't crash if binary junk is inside the range.
                content = raw_bytes.decode("utf-8", errors="ignore")
                
                # Write exactly what we found + a newline to separate from next doc
                fout.write(content + "\n")

    print(f"\n🎉 Done! Saved to {OUTPUT_FILE}")
    if os.path.exists(OUTPUT_FILE):
        size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
        print(f"📂 New File Size: {size_mb:.2f} MB")

if __name__ == "__main__":
    create_subset()