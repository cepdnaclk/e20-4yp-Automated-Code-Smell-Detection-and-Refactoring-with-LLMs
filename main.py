import json

from config import DEFAULT_OUTPUT_PATH, INPUT_ANALYSIS_PATH, UPLOADS_DIR
from pipeline.orchestrator import _model_dump_json, run_pipeline


def load_analysis():
    with INPUT_ANALYSIS_PATH.open(encoding="utf-8-sig") as handle:
        return json.load(handle)


def build_payload(analysis):
    file_name = analysis.get("file_name", "sample.py")
    language = analysis.get("language", "Python")
    code = analysis.get("code")

    if code is None:
        upload_path = UPLOADS_DIR / file_name
        if upload_path.exists():
            code = upload_path.read_text(encoding="utf-8")

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

