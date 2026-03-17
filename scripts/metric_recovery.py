import pandas as pd
import subprocess
import os
import shutil

# --- CONFIGURATION ---
INPUT_CSV = r"E:\FYP_Project\gold_standard_for_llm.csv"
OUTPUT_CSV = r"E:\FYP_Project\gold_standard_27_metrics.csv"
CK_JAR_PATH = r"E:\FYP_Project\tools\ck.jar"
TEMP_DIR = r"E:\FYP_Project\temp_processing"

# --- YOUR HELPER FUNCTION ---
def recover_27_metrics(source_code, file_name="TempClass.java"):
    """
    Runs the CK Tool on a single string of Java code.
    Returns: Dictionary of metrics (cbo, wmc, rfc, lcom, etc.)
    """
    # 1. Prepare Temp Directory
    if os.path.exists(TEMP_DIR):
        try:
            shutil.rmtree(TEMP_DIR)
        except:
            pass # Ignore errors if file is locked
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # 2. Save Code to File
    # Sanitize filename to avoid errors with special characters
    safe_name = "".join([c for c in file_name if c.isalnum()])
    if not safe_name: safe_name = "TempClass"
    
    java_file_path = os.path.join(TEMP_DIR, f"{safe_name}.java")
    
    try:
        with open(java_file_path, "w", encoding="utf-8") as f:
            f.write(str(source_code))
            
        # 3. Run the CK Tool (Java)
        # cmd: java -jar ck.jar <input_dir> <use_jars> <max_files> <output_dir>
        cmd = ["java", "-jar", CK_JAR_PATH, TEMP_DIR, "false", "0", "False", TEMP_DIR]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # 4. Read the Result
        output_csv = os.path.join(TEMP_DIR, "class.csv")
        if os.path.exists(output_csv):
            df = pd.read_csv(output_csv)
            if not df.empty:
                # Return the first row as a dictionary
                return df.iloc[0].to_dict()
                
    except Exception as e:
        # print(f"⚠️ Error processing {file_name}: {e}") # Uncomment to debug
        pass
            
    # Return empty/zero metrics if anything failed
    return {"loc": 0, "wmc": 0, "rfc": 0, "cbo": 0, "lcom": 0}

# --- MAIN DRIVER CODE ---
def main():
    print("🚀 STARTING METRIC RECOVERY PIPELINE")
    print(f"Reading from: {INPUT_CSV}")
    
    # 1. Load the Dataset
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"Found {len(df)} rows. This might take a while...")
    except FileNotFoundError:
        print("❌ Error: Input CSV not found!")
        return

    # 2. Process Every Row
    all_metrics = []
    
    for index, row in df.iterrows():
        # Feedback every 50 rows so you know it's working
        if (index + 1) % 50 == 0:
            print(f"   -> Processing row {index + 1}/{len(df)}...")

        # Get code and run your function
        code = row.get('source_code', '')
        name = str(row.get('class_name', 'Temp'))
        
        metrics = recover_27_metrics(code, name)
        all_metrics.append(metrics)

    # 3. Create DataFrame from Results
    print("Merging results...")
    metrics_df = pd.DataFrame(all_metrics)
    
    # 4. Merge with Original Data
    # We combine the original columns (class_name, smells, code) with the new metrics
    # If the original CSV already had 'metrics', we drop it to avoid confusion
    if 'metrics' in df.columns:
        df = df.drop(columns=['metrics'])
        
    final_df = pd.concat([df, metrics_df], axis=1)

    # 5. Save
    final_df.to_csv(OUTPUT_CSV, index=False)
    print(f"✅ DONE! Saved new dataset to: {OUTPUT_CSV}")
    print("New columns include:", list(metrics_df.columns[:10]), "...")

if __name__ == "__main__":
    main()