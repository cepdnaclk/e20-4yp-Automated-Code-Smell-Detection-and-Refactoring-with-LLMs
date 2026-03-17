import json
from pathlib import Path

from config import DEFAULT_OUTPUT_PATH, INPUT_ANALYSIS_PATH, UPLOADS_DIR
from pipeline.orchestrator import _model_dump_json, run_pipeline
from rules.strategy_selector import normalize_smell_name

DETECTION_TO_REFACTOR_ALIASES = {
    "Large Class": "Excessive Class Length",
    "God Class": "Blob (God Class)",
    "Blob": "Blob (God Class)",
    "Long Function": "Long Method",
}

SUPPORTED_REFACTOR_SMELLS = {
    "Magic Number",
    "Blob (God Class)",
    "Data Class",
    "Long Method",
    "Feature Envy",
    "Shotgun Surgery",
    "Divergent Change",
    "Lazy Class",
    "Refused Bequest",
    "Middle Man",
    "Message Chains",
    "Long Parameter List",
    "Primitive Obsession",
    "Switch Statements",
    "Speculative Generality",
    "Temporary Field",
    "Data Clumps",
    "Inappropriate Intimacy",
    "Duplicate Code",
    "Complex Conditional",
    "Dead Code",
    "Complex Method",
    "Excessive Class Length",
    "Excessive Method Length",
    "Excessive Return Statements",
    "Excessive Coupling",
    "Excessive Public Fields",
    "Excessive Static Fields",
}


def load_analysis():
    with INPUT_ANALYSIS_PATH.open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def _infer_language(file_name: str) -> str:
    suffix = Path(file_name).suffix.lower()
    if suffix == ".java":
        return "Java"
    return "Python"


def _normalize_detection_smell(smell_name: str) -> str:
    mapped = DETECTION_TO_REFACTOR_ALIASES.get(smell_name.strip(), smell_name.strip())
    return normalize_smell_name(mapped)


def _convert_detected_smells_analysis(analysis):
    file_name = analysis.get("file_name", "detected_input.java")
    language = analysis.get("language") or _infer_language(file_name)
    code = analysis.get("code")
    smells = []
    priority_order = {}
    priority_metadata = {}

    for index, item in enumerate(analysis.get("priority_list", [])):
        normalized = _normalize_detection_smell(item.get("smell", ""))
        if not normalized:
            continue
        priority_order.setdefault(normalized, index)
        priority_metadata.setdefault(normalized, item)

    for item in analysis.get("detected_smells", []):
        normalized = _normalize_detection_smell(item.get("smell", ""))
        if normalized not in SUPPORTED_REFACTOR_SMELLS:
            continue
        priority_item = priority_metadata.get(normalized, {})
        smells.append(
            {
                "type": normalized,
                "severity": priority_item.get("severity", "Moderate"),
                "location": item.get("location") or priority_item.get("location") or "unknown",
                "metrics": {
                    "supported_by": item.get("supported_by", []),
                    "category": priority_item.get("category", analysis.get("category")),
                    "priority_score": priority_item.get("priority_score"),
                    "smell_weight": priority_item.get("smell_weight"),
                },
            }
        )

    smells.sort(key=lambda item: priority_order.get(item["type"], len(priority_order)))

    return {
        "file_name": file_name,
        "language": language,
        "code": code,
        "smells": smells,
    }


def _convert_priority_list_analysis(analysis):
    file_name = analysis.get("file_name", "detected_input.java")
    language = analysis.get("language") or _infer_language(file_name)
    code = analysis.get("code")
    smells = []

    for item in analysis.get("priority_list", []):
        normalized = _normalize_detection_smell(item.get("smell", ""))
        if normalized not in SUPPORTED_REFACTOR_SMELLS:
            continue
        smells.append(
            {
                "type": normalized,
                "severity": item.get("severity", "Moderate"),
                "location": item.get("location") or "unknown",
                "metrics": {
                    "supported_by": item.get("supported_by", []),
                    "priority_score": item.get("priority_score"),
                    "category": item.get("category"),
                },
            }
        )

    return {
        "file_name": file_name,
        "language": language,
        "code": code,
        "smells": smells,
    }


def build_payload(analysis):
    if "detected_smells" in analysis and "smells" not in analysis:
        analysis = _convert_detected_smells_analysis(analysis)
    elif "priority_list" in analysis and "smells" not in analysis:
        analysis = _convert_priority_list_analysis(analysis)

    file_name = analysis.get("file_name", "sample.py")
    language = analysis.get("language", "Python")
    code = analysis.get("code")

    if code is None:
        upload_path = UPLOADS_DIR / file_name
        if upload_path.exists():
            code = upload_path.read_text(encoding="utf-8-sig")

    return {
        "file_name": file_name,
        "language": language,
        "code": code,
        "smells": analysis.get("smells", []),
    }


def main():
    analysis = load_analysis()
    payload = build_payload(analysis)
    output = run_pipeline(payload, DEFAULT_OUTPUT_PATH)

    print("\n--- REFACTORING SUMMARY ---\n")
    print(_model_dump_json(output.summary, indent=2))
    print(f"\nDetailed results written to: {DEFAULT_OUTPUT_PATH}")


if __name__ == "__main__":
    main()
