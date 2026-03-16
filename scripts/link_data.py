import pandas as pd
import os
import glob

# --- CONFIGURATION ---
# Path to your 58 CSV parts (Update if they are in a subfolder)
CSV_PATTERN = r"E:\FYP_Project\dataset\qscored_ml_part*" 
# Path where you cloned junit4, checkstyle, etc.
SOURCE_ROOT = r"E:\FYP_Project\source_repos"
# The file we will save for the LLM
OUTPUT_FILE = "gold_standard_for_llm.csv"

def find_code_locally(class_name, root_dir):
    """Searches for ClassName.java in the source_repos folder"""
    target = f"{class_name}.java"
    for root, dirs, files in os.walk(root_dir):
        if target in files:
            return os.path.join(root, target)
    return None

def main():
    # 1. Get all 58 CSV files
    csv_files = glob.glob(CSV_PATTERN)
    print(f"Found {len(csv_files)} CSV data parts.")
    
    linked_data = []
    
    # 2. Process the first 5 files (To save time for testing)
    # Change [:5] to separate logic if you want all of them later
    for f in csv_files[:5]: 
        print(f"Reading {os.path.basename(f)}...")
        try:
            df = pd.read_csv(f, encoding='utf-8', on_bad_lines='skip')
            
            # 3. For each row, try to find the Java file
            for idx, row in df.iterrows():
                class_name = str(row.get('class_name', '')).strip()
                if not class_name: continue
                
                # Search for the file
                code_path = find_code_locally(class_name, SOURCE_ROOT)
                
                if code_path:
                    try:
                        with open(code_path, 'r', encoding='utf-8', errors='ignore') as code_file:
                            source_code = code_file.read()
                            
                        # Success! We matched Data + Code
                        linked_data.append({
                            'class_name': class_name,
                            'metrics': f"LOC:{row.get('loc')}, WMC:{row.get('wmc')}",
                            'actual_smells': row.get('design_smells'),
                            'source_code': source_code
                        })
                    except:
                        pass # Skip unreadable files
                        
        except Exception as e:
            print(f"Skipping {f} due to error: {e}")

    # 4. Save the Result
    if linked_data:
        final_df = pd.DataFrame(linked_data)
        final_df.to_csv(OUTPUT_FILE, index=False)
        print(f"\nSUCCESS! Created {OUTPUT_FILE} with {len(linked_data)} samples.")
        print("You can now run the LLM detection on this file.")
    else:
        print("\nWARNING: No matching code found. Did you clone the repos in Step 2?")

if __name__ == "__main__":
    main()