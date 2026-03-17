import joblib
import pandas as pd
import subprocess

MODEL_PATH = "backend/models/ml_smell_model.pkl"

model = joblib.load(MODEL_PATH)


def extract_metrics():

    subprocess.run([
        "java",
        "-jar",
        "tools/ck.jar",
        "temp_processing",
        "true",
        "0",
        "false"
    ])

    df = pd.read_csv("class.csv")
    return df


def detect_metric(java_file):

    df = extract_metrics()

    if df is None:
        return []

    smells = []

    try:
        features = df[["WMC", "CBO", "LOC", "LCOM", "RFC"]]

        predictions = model.predict(features)

        for pred in predictions:

            if pred == 1:
                smells.append("Large Class")

            elif pred == 2:
                smells.append("Complex Method")

            elif pred == 3:
                smells.append("God Class")

            elif pred == 4:
                smells.append("Feature Envy")

            elif pred == 5:
                smells.append("Data Class")

            elif pred == 6:
                smells.append("Lazy Class")

    except:
        pass

    return list(set(smells))