import pandas as pd
from openai import OpenAI
import json
import time

# --- CONFIGURATION ---
INPUT_FILE = r"E:\FYP_Project\gold_standard_for_llm.csv"
OUTPUT_FILE = r"E:\FYP_Project\ollama_results.csv"

# --- OLLAMA SETUP ---
# Ollama runs locally on port 11434
client = OpenAI(
    base_url='http://localhost:11434/v1',
    api_key='ollama', # specific key doesn't matter for local ollama
)

# Use the model you pulled in Step 2
MODEL_NAME = "deepseek-coder" 

def analyze_code_locally(code, metrics):
    prompt = f"""
    You are an expert code reviewer. Analyze this Java code for 3 specific smells:
    1. Long Method
    2. Feature Envy
    3. Magic Strings
    
    METRICS provided: {metrics}
    
    CODE:
    {code[:4000]} 
    
    Return ONLY a JSON object with this format (no other text):
    {{
        "smells": ["List detected smells here"],
        "severity": "High/Medium/Low",
        "reason": "Brief explanation"
    }}
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a JSON-only code analysis tool."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def main():
    print("--- STARTING LOCAL DETECTION (DEEPSEEK) ---")
    
    # Load your data (created in the previous step)
    df = pd.read_csv(INPUT_FILE)
    
    # Let's test just 5 rows first because local CPU/GPU can be slower
    subset = df.head(5).copy()
    
    print(f"Analyzing {len(subset)} rows with local {MODEL_NAME}...")
    
    results = []
    for index, row in subset.iterrows():
        print(f"[{index+1}/{len(subset)}] Processing {row['class_name']}...")
        
        # Call Ollama
        output = analyze_code_locally(row['source_code'], row['metrics'])
        
        print(f"   -> Result: {output[:50]}...") # Print first 50 chars to show it's working
        results.append(output)

    subset['llm_output'] = results
    subset.to_csv(OUTPUT_FILE, index=False)
    print(f"\n✅ Done! Check {OUTPUT_FILE}")

if __name__ == "__main__":
    main()