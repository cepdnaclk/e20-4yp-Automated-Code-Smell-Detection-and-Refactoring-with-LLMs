import json
from pathlib import Path
from typing import Any, Dict, Optional

from config import DEFAULT_OUTPUT_PATH, OUTPUTS_DIR, UPLOADS_DIR
from llm.client import call_llm
from llm.prompt_runner import build_refactor_prompt, build_repair_prompt
from metrics.code_metrics import compare_metrics
from models.schemas import RefactorInput, RefactorOutput, RefactorResult, Summary
from rules.strategy_selector import get_strategy, load_catalog, sort_smells
from utils.code_scope import build_scope_note, extract_focus_scope
from validators.common import validate_code

DEFAULT_PLAN_SUMMARY = "Direct refactoring mode enabled; apply the strategy conservatively within the focused scope."


def _model_validate(model_class, payload: Dict[str, Any]):
    if hasattr(model_class, "model_validate"):
        return model_class.model_validate(payload)
    return model_class.parse_obj(payload)


def _model_dump(model) -> Dict[str, Any]:
    if hasattr(model, "model_dump"):
        return model.model_dump()
    return model.dict()


def _model_dump_json(model, indent: int = 2) -> str:
    if hasattr(model, "model_dump_json"):
        return model.model_dump_json(indent=indent)
    return model.json(indent=indent)


def _load_code(payload: RefactorInput) -> str:
    if payload.code:
        return payload.code
    upload_path = UPLOADS_DIR / payload.file_name
    if upload_path.exists():
        return upload_path.read_text(encoding="utf-8")
    raise FileNotFoundError(f"Unable to locate code for {payload.file_name}")


def _build_context(
    payload: RefactorInput,
    smell: dict,
    strategy_meta: dict,
    code: str,
    focused_scope: str,
    scope_note: str,
    errors: str = "",
    invalid_output: str = "",
) -> dict:
    return {
        "LANGUAGE": payload.language,
        "FILE_NAME": payload.file_name,
        "SMELL_TYPE": smell["type"],
        "SEVERITY": smell.get("severity", "Moderate"),
        "LOCATION": smell.get("location") or "unknown",
        "METRICS": json.dumps(smell.get("metrics", {}), ensure_ascii=True),
        "CATEGORY": strategy_meta.get("category", "unknown"),
        "GROUP": strategy_meta.get("group", "unknown"),
        "STRATEGY": strategy_meta["primary_strategy"],
        "FALLBACK_STRATEGIES": ", ".join(strategy_meta.get("fallback_strategies", [])),
        "RAW_CODE": code,
        "FOCUSED_SCOPE": focused_scope,
        "SCOPE_NOTE": scope_note,
        "PLAN_SUMMARY": DEFAULT_PLAN_SUMMARY,
        "PLAN_OUTPUT_CONTRACT": "Plan stage disabled.",
        "ERRORS": errors,
        "INVALID_OUTPUT": invalid_output,
    }


def _run_single_refactor(
    payload: RefactorInput,
    original_code: str,
    smell: dict,
    catalog: dict,
    llm_model_override: Optional[str] = None,
) -> RefactorResult:
    strategy_meta = get_strategy(smell["type"], catalog)
    focused_scope = extract_focus_scope(original_code, smell.get("location") or "", smell.get("metrics", {}))
    scope_note = build_scope_note(smell.get("location") or "unknown", focused_scope, original_code)

    context = _build_context(
        payload,
        smell,
        strategy_meta,
        original_code,
        focused_scope,
        scope_note,
    )
    prompt = build_refactor_prompt(context)
    response = call_llm(prompt, model_override=llm_model_override)
    validation = validate_code(response, payload.language, strategy_meta["validation_level"])

    if not validation.syntax:
        repair_context = _build_context(
            payload,
            smell,
            strategy_meta,
            original_code,
            focused_scope,
            scope_note,
            errors="\n".join(validation.errors),
            invalid_output=response,
        )
        repair_prompt = build_repair_prompt(repair_context)
        repaired_response = call_llm(repair_prompt, model_override=llm_model_override)
        repaired_validation = validate_code(
            repaired_response,
            payload.language,
            strategy_meta["validation_level"],
        )
        response = repaired_response
        validation = repaired_validation

    status = "success" if validation.syntax else "failed"
    rationale = (
        f"Applied {strategy_meta['primary_strategy']} for {smell['type']} "
        f"within {strategy_meta.get('group', 'unknown')}."
    )
    metrics = compare_metrics(original_code, response) if validation.syntax else {}

    return RefactorResult(
        smell_type=smell["type"],
        strategy=strategy_meta["primary_strategy"],
        status=status,
        rationale=rationale,
        original_code=original_code,
        refactored_code=response,
        validation=validation,
        metrics=metrics,
        category=strategy_meta.get("category"),
        group=strategy_meta.get("group"),
        location=smell.get("location"),
        severity=smell.get("severity"),
        focused_scope=focused_scope,
        refactoring_plan=DEFAULT_PLAN_SUMMARY,
    )


def run_pipeline(
    payload_data: dict,
    output_path: Path = DEFAULT_OUTPUT_PATH,
    llm_model_override: Optional[str] = None,
) -> RefactorOutput:
    payload = _model_validate(RefactorInput, payload_data)
    catalog = load_catalog()
    original_code = _load_code(payload)
    sorted_smells = sort_smells([_model_dump(smell) for smell in payload.smells], catalog)

    results = [
        _run_single_refactor(payload, original_code, smell, catalog, llm_model_override=llm_model_override)
        for smell in sorted_smells
    ]
    success_count = sum(1 for result in results if result.status == "success")
    output = RefactorOutput(
        file_name=payload.file_name,
        language=payload.language,
        results=results,
        summary=Summary(
            smells_received=len(payload.smells),
            smells_refactored=success_count,
            failures=len(payload.smells) - success_count,
        ),
    )

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path.write_text(_model_dump_json(output, indent=2), encoding="utf-8")
    return output
