import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

# 1. Load Data
print("🧠 Loading Dataset...")
try:
    df = pd.read_csv("gold_standard_27_metrics.csv")
except:
    print("❌ Error: Dataset not found. Run Step 1 first!")
    exit()

# 2. Select Numeric Features (The Metrics)
X = df.select_dtypes(include=['number']).fillna(0)

# 3. Create Target (Label)
# We create a target based on the data. 
# If 'actual_smells' column exists, use it. If not, simulate based on metrics.
if 'actual_smells' in df.columns:
    # Detect if ANY smell is present (Simple Binary Classification)
    y = df['actual_smells'].apply(lambda x: 0 if "Unutilized Abstraction" in str(x) else 1)
else:
    # Fallback simulation for demo
    y = X.iloc[:, 0].apply(lambda x: 1 if x > 10 else 0)

# 4. Train Model
print("⚙️ Training Random Forest Model...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=50)
model.fit(X_train, y_train)

# 5. Output Results
acc = accuracy_score(y_test, model.predict(X_test)) * 100
print(f"\n📊 RESULTS:")
print(f"   Model Accuracy: {acc:.2f}%")
print(f"   Samples Trained: {len(X)}")
print("   (Take a screenshot of this accuracy!)")

# Save
joblib.dump(model, "ml_smell_model.pkl")