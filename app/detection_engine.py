from app.static_detector import detect_static
from app.ml_detector import detect_metric
from app.llm_detector import detect_llm

def detect_all_smells(java_file):

    with open(java_file) as f:
        code = f.read()

    static_smells = detect_static(code)

    metric_smells = detect_metric(java_file)

    llm_smells = detect_llm(code)

    return {

        "static_engine": static_smells,
        "metric_engine": metric_smells,
        "llm_engine": llm_smells

    }