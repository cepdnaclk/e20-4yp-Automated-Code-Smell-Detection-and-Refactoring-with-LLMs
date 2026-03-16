import json
import re
from pathlib import Path
from typing import Dict, Optional

from config import PROMPTS_DIR
from llm.example_loader import format_examples, select_examples


STRATEGY_GUIDANCE = {
    "extract_method": [
        "Extract cohesive blocks into clearly named helper methods.",
        "Keep the main method shorter and easier to read.",
        "Avoid changing externally visible behavior.",
    ],
    "extract_class": [
        "Split unrelated responsibilities into a new focused class.",
        "Move only the fields and methods that belong together.",
        "Preserve the original collaboration flow as much as possible.",
    ],
    "move_method": [
        "Move behavior closer to the data it uses most.",
        "Reduce unnecessary cross-object access.",
        "Keep call sites simple and behavior-preserving.",
    ],
    "move_field": [
        "Move state to the owning class that uses it most naturally.",
        "Do not duplicate state across classes.",
    ],
    "inline_method_or_class": [
        "Remove indirection only when it adds little value.",
        "Keep the simplified structure readable and minimal.",
    ],
    "introduce_parameter_object": [
        "Group related parameters into a meaningful object.",
        "Use a clear domain name for the new parameter object.",
        "Keep call-site changes minimal and consistent.",
    ],
    "replace_primitive_with_value_object": [
        "Replace loosely related primitive values with a domain object or enum.",
        "Improve clarity without expanding scope beyond the smell.",
    ],
    "replace_conditional_with_polymorphism": [
        "Replace type-based branching with polymorphic behavior when appropriate.",
        "Keep the resulting design small and understandable.",
    ],
    "decompose_conditional": [
        "Break complex conditionals into intention-revealing helper methods.",
        "Prefer readable guard clauses or well-named checks.",
    ],
    "encapsulate_field": [
        "Reduce direct field exposure and protect invariants.",
        "Add accessors only where needed for compatibility.",
    ],
    "remove_dead_code": [
        "Remove unreachable, unused, or redundant code only.",
        "Do not remove code that still affects behavior.",
    ],
    "reduce_coupling": [
        "Minimize unnecessary knowledge between classes or modules.",
        "Prefer cleaner boundaries over large structural rewrites.",
    ],
    "replace_inheritance_with_delegation": [
        "Prefer delegation when inheritance is forcing unrelated behavior.",
        "Preserve the public contract where possible.",
    ],
    "split_responsibilities": [
        "Separate unrelated reasons to change into distinct units.",
        "Aim for cohesive responsibilities rather than cosmetic extraction.",
    ],
}

SMELL_GUIDANCE = {
    "blob_god_class": [
        "Extract one coherent responsibility into a collaborator instead of rewriting the entire class.",
        "Move only the fields and methods needed by the extracted responsibility.",
    ],
    "long_method": [
        "Target the largest cohesive block first and preserve the original method signature.",
        "Prefer a small number of well-named helpers over a full rewrite.",
    ],
    "feature_envy": [
        "Move behavior toward the class whose data is accessed most heavily.",
        "Leave a thin delegating wrapper only if removing the original method would break callers.",
    ],
    "duplicate_code": [
        "Extract the shared logic once and keep call sites simple.",
        "Do not over-generalize beyond the duplicated behavior already present.",
    ],
    "complex_conditional": [
        "Name the decision rules explicitly using helper predicates or guard clauses.",
        "Keep the decision order and branching semantics unchanged.",
    ],
    "long_parameter_list": [
        "Create one meaningful request or value object for parameters that travel together.",
        "Avoid introducing multiple wrapper objects unless the smell clearly demands it.",
    ],
    "primitive_obsession": [
        "Replace raw primitives with one small domain type that owns validation or formatting.",
        "Keep the new value object lightweight and directly relevant to the smell.",
    ],
    "data_clumps": [
        "Identify the repeated parameter cluster and give it a domain name.",
        "Refactor all touched call sites consistently for that cluster.",
    ],
    "dead_code": [
        "Remove only code proven unused or unreachable in the provided context.",
        "Do not invent new behavior while cleaning up dead paths.",
    ],
    "excessive_coupling": [
        "Hide deep navigation behind one intention-revealing method or boundary.",
        "Reduce knowledge of collaborator internals without broad architectural rewrites.",
    ],
}

LANGUAGE_RULES = {
    "python": [
        "Return valid Python code only.",
        "Keep indentation consistent and syntactically correct.",
        "Prefer small helper functions over unnecessary classes unless the strategy needs a class.",
    ],
    "java": [
        "Return valid Java code only.",
        "Preserve class and method declarations unless the refactoring requires structural movement.",
        "Keep imports, visibility, and braces consistent.",
    ],
}


def _load_prompt(path: Path) -> Optional[str]:
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8-sig")


def _render(template: str, context: Dict[str, str]) -> str:
    rendered = template
    for key, value in context.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    return rendered


def _render_bullets(items):
    if not items:
        return "- No additional guidance"
    return "\n".join(f"- {item}" for item in items)


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def _parse_metrics(metrics: str):
    try:
        return json.loads(metrics) if metrics else {}
    except json.JSONDecodeError:
        return {}


def _enrich_context(context: Dict[str, str]) -> Dict[str, str]:
    language = context["LANGUAGE"].lower()
    strategy = context["STRATEGY"]
    smell_slug = _slugify(context["SMELL_TYPE"])
    metrics = _parse_metrics(context.get("METRICS", ""))
    example_target = context.get("FOCUSED_SCOPE") or context.get("RAW_CODE", "")
    examples = select_examples(
        language,
        strategy,
        context["SMELL_TYPE"],
        target_code=example_target,
        location=context.get("LOCATION", ""),
        metrics=metrics,
    )
    enriched = dict(context)
    enriched["LANGUAGE_RULES"] = _render_bullets(LANGUAGE_RULES.get(language, []))
    enriched["STRATEGY_GUIDANCE"] = _render_bullets(STRATEGY_GUIDANCE.get(strategy, []))
    enriched["SMELL_GUIDANCE"] = _render_bullets(SMELL_GUIDANCE.get(smell_slug, []))
    enriched["FEW_SHOT_EXAMPLES"] = format_examples(examples)
    enriched["REFACTORING_GOAL"] = (
        f"Refactor the code at or around {context['LOCATION']} to address "
        f"the smell {context['SMELL_TYPE']} using {strategy}."
    )
    enriched["OUTPUT_CONTRACT"] = (
        "Return only the final refactored code. Do not include explanations, markdown fences, "
        "headings, or analysis text."
    )
    enriched.setdefault("FOCUSED_SCOPE", context.get("RAW_CODE", ""))
    enriched.setdefault("SCOPE_NOTE", "No focused scope provided.")
    enriched.setdefault("PLAN_SUMMARY", "No plan available; apply the strategy conservatively.")
    enriched.setdefault("PLAN_OUTPUT_CONTRACT", "Return concise planning notes using the requested headings.")
    return enriched


def _select_refactor_template(language: str, strategy: str, smell_slug: str) -> Optional[str]:
    return (
        _load_prompt(PROMPTS_DIR / language / "smells" / f"{smell_slug}.txt")
        or _load_prompt(PROMPTS_DIR / "base" / "smells" / f"{smell_slug}.txt")
        or _load_prompt(PROMPTS_DIR / language / f"{strategy}.txt")
        or _load_prompt(PROMPTS_DIR / "base" / f"{strategy}.txt")
        or _load_prompt(PROMPTS_DIR / "base" / "system_refactor.txt")
    )


def build_plan_prompt(context: Dict[str, str]) -> str:
    template = _load_prompt(PROMPTS_DIR / "base" / "plan_refactor.txt")
    if not template:
        raise FileNotFoundError("Plan prompt template not found")
    return _render(template, _enrich_context(context))


def build_refactor_prompt(context: Dict[str, str]) -> str:
    language = context["LANGUAGE"].lower()
    strategy = context["STRATEGY"]
    smell_slug = _slugify(context["SMELL_TYPE"])
    template = _select_refactor_template(language, strategy, smell_slug)
    if not template:
        raise FileNotFoundError("No refactoring prompt templates found")
    return _render(template, _enrich_context(context))


def build_repair_prompt(context: Dict[str, str]) -> str:
    template = _load_prompt(PROMPTS_DIR / "base" / "repair_prompt.txt")
    if not template:
        raise FileNotFoundError("Repair prompt template not found")
    return _render(template, _enrich_context(context))
