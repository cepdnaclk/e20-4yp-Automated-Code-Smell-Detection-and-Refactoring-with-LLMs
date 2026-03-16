import json
import time
from datetime import datetime
from pathlib import Path

from config import DEFAULT_OUTPUT_PATH, EXPERIMENTS_DIR, LLM_PROVIDER, OLLAMA_MODELS
from main import build_payload, load_analysis
from pipeline.orchestrator import _model_dump, _model_dump_json, run_pipeline


def _safe_model_slug(name: str) -> str:
    return "".join(ch.lower() if ch.isalnum() else "_" for ch in name).strip("_")


def _select_models():
    if LLM_PROVIDER == "ollama":
        return OLLAMA_MODELS
    return ["provider_default"]


def main():
    analysis = load_analysis()
    payload = build_payload(analysis)
    models = _select_models()

    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    experiment_results = []

    for model_name in models:
        started = time.perf_counter()
        model_slug = _safe_model_slug(model_name)
        output_path = EXPERIMENTS_DIR / f"{timestamp}_{model_slug}.json"

        try:
            output = run_pipeline(
                payload,
                output_path=output_path,
                llm_model_override=(model_name if LLM_PROVIDER == "ollama" else None),
            )
            duration_seconds = round(time.perf_counter() - started, 2)
            summary = _model_dump(output.summary)
            smell_results = [_model_dump(result) for result in output.results]
            experiment_results.append(
                {
                    "model": model_name,
                    "provider": LLM_PROVIDER,
                    "status": "completed",
                    "duration_seconds": duration_seconds,
                    "summary": summary,
                    "output_path": str(output_path),
                    "result_breakdown": [
                        {
                            "smell_type": result["smell_type"],
                            "status": result["status"],
                            "syntax": result["validation"]["syntax"],
                            "error_count": len(result["validation"]["errors"]),
                        }
                        for result in smell_results
                    ],
                }
            )
        except Exception as exc:
            duration_seconds = round(time.perf_counter() - started, 2)
            experiment_results.append(
                {
                    "model": model_name,
                    "provider": LLM_PROVIDER,
                    "status": "failed",
                    "duration_seconds": duration_seconds,
                    "error": str(exc),
                }
            )

    report = {
        "provider": LLM_PROVIDER,
        "file_name": payload["file_name"],
        "language": payload["language"],
        "models_tested": models,
        "smells_requested": [smell["type"] for smell in payload["smells"]],
        "runs": experiment_results,
    }

    latest_path = EXPERIMENTS_DIR / "latest_experiment.json"
    latest_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("\n--- EXPERIMENT SUMMARY ---\n")
    print(json.dumps(report, indent=2))
    print(f"\nDetailed experiment report written to: {latest_path}")


if __name__ == "__main__":
    main()
