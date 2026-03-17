import subprocess
import pandas as pd


def extract_metrics(java_file):

    try:

        cmd = [
            "java",
            "-jar",
            "tools/ck.jar",
            "temp_processing",
            "true",
            "0",
            "false"
        ]

        subprocess.run(cmd)

        df = pd.read_csv("class.csv")

        return df

    except:
        return None


def detect_metric(java_file):

    df = extract_metrics(java_file)

    if df is None:
        return []

    smells = []

    try:

        if df["WMC"].iloc[0] > 50:
            smells.append("Complex Method")

        if df["LOC"].iloc[0] > 500:
            smells.append("Large Class")

        if df["CBO"].iloc[0] > 14:
            smells.append("Hub Like Dependency")

    except:
        pass

    return smells