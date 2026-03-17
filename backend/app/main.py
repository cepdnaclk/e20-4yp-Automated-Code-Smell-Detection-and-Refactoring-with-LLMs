import json
import logging
import os
import shutil
import sys
from typing import Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("data/app_server.log")
    ]
)
logger = logging.getLogger(__name__)

try:
    from fastapi import FastAPI, UploadFile, File
    from backend.app.detection_engine import detect_all_smells
    from backend.app.result_consolidator import consolidate_results
    from backend.app.smell_analyzer import run_smell_analysis_pipeline
    import main as refactoring_entry
    from pipeline.orchestrator import _model_dump, run_pipeline
except Exception as e:
    logger.error(f"Import error: {e}")
    sys.exit(1)

app = FastAPI()


def _infer_language(file_name: str) -> str:
    return "Java" if file_name.lower().endswith(".java") else "Python"


def _build_detected_payload(file_name: str, code: str, consolidation: dict, final_result: Optional[dict] = None) -> dict:
    return {
        "file_name": file_name,
        "language": _infer_language(file_name),
        "code": code,
        "detected_smells": consolidation.get("candidate_smells", []),
        "engine_summary": consolidation.get("engine_summary", {}),
        "primary_smell": consolidation.get("primary_smell"),
        "category": consolidation.get("category"),
        "priority_list": (final_result or {}).get("priority_list", []),
    }


def _save_detected_smells(file_name: str, code: str, consolidation: dict, final_result: Optional[dict] = None) -> dict:
    detected_payload = _build_detected_payload(file_name, code, consolidation, final_result)
    os.makedirs("detection_results", exist_ok=True)
    with open("detection_results/detected_smells.json", "w", encoding="utf-8") as handle:
        json.dump(detected_payload, handle, indent=2)
    logger.info("Detected smells written to detection_results/detected_smells.json")
    return detected_payload


def _run_refactoring(detected_payload: dict) -> dict:
    refactor_payload = refactoring_entry.build_payload(detected_payload)
    refactor_output = run_pipeline(refactor_payload)
    return _model_dump(refactor_output)


def _save_refactoring_handoff(file_name: str, code: str, final_result: dict) -> None:
    handoff_payload = {
        "file_name": file_name,
        "language": _infer_language(file_name),
        "code": code,
        "priority_list": final_result.get("priority_list", []),
        "engine_summary": final_result.get("engine_summary", {}),
    }
    os.makedirs("detection_results", exist_ok=True)
    with open("detection_results/from_detection.json", "w", encoding="utf-8") as handle:
        json.dump(handoff_payload, handle, indent=2)
    logger.info("Refactoring handoff written to detection_results/from_detection.json")


@app.get("/")
def home():
    logger.info("Root endpoint hit")
    return {"message": "SmellSense AI running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    logger.info(f"Received file for analysis: {file.filename}")
    try:
        os.makedirs("temp_processing", exist_ok=True)
        file_path = f"temp_processing/{file.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info("Running detection engines...")
        engine_results = detect_all_smells(file_path)

        logger.info("Running analysis pipeline...")
        with open(file_path, encoding="utf-8-sig") as f:
            code = f.read()

        consolidation = consolidate_results(engine_results)
        final_result = run_smell_analysis_pipeline(engine_results, code)
        logger.info("Analysis complete")

        smell_names = [item["smell"] for item in final_result.get("priority_list", [])]
        with open("data/priority_list.json", "w", encoding="utf-8") as f:
            json.dump(smell_names, f, indent=4)
        logger.info("Priority smell names saved to data/priority_list.json")

        detected_payload = _save_detected_smells(file.filename, code, consolidation, final_result)
        _save_refactoring_handoff(file.filename, code, final_result)
        refactoring_result = _run_refactoring(detected_payload)
        return {
            **final_result,
            "detected_smells": detected_payload.get("detected_smells", []),
            "refactoring": refactoring_result,
        }
    except Exception as e:
        logger.exception("Error during analysis")
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    logger.info("Starting uvicorn server on port 8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
