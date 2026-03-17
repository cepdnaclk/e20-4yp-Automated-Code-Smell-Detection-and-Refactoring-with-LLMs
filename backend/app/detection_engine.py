from backend.app.static_detector import detect_static
from backend.app.ml_detector import detect_metric
from backend.app.llm_detector import detect_llm
import logging

logger = logging.getLogger(__name__)

def detect_all_smells(java_file):
    with open(java_file) as f:
        code = f.read()

    logger.info("Starting static detection...")
    static_smells = detect_static(code)
    logger.info(f"Static smells: {static_smells}")

    logger.info("Starting metric detection...")
    metric_smells = detect_metric(java_file)
    logger.info(f"Metric smells: {metric_smells}")

    logger.info("Starting LLM detection...")
    llm_smells = detect_llm(code)
    logger.info(f"LLM smells: {llm_smells}")

    return {
        "static_engine": static_smells,
        "metric_engine": metric_smells,
        "llm_engine": llm_smells
    }