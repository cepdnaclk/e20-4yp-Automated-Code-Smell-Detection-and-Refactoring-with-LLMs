import re
from typing import Any, Dict, List


CONTROL_FLOW_KEYWORDS = ("if ", "elif ", "for ", "while ", "case ", "catch ", "&&", "||")


def _non_empty_lines(code: str) -> List[str]:
    return [line for line in code.splitlines() if line.strip()]


def _estimate_parameter_count(code: str) -> int:
    match = re.search(r"\((.*?)\)", code, re.DOTALL)
    if not match:
        return 0
    params = [part.strip() for part in match.group(1).split(",") if part.strip()]
    return len(params)


def _estimate_complexity(code: str) -> int:
    complexity = 1
    for line in code.splitlines():
        stripped = line.strip()
        if any(keyword in stripped for keyword in CONTROL_FLOW_KEYWORDS):
            complexity += 1
    return complexity


def compute_code_metrics(code: str) -> Dict[str, Any]:
    lines = _non_empty_lines(code)
    return {
        "loc": len(lines),
        "parameter_count": _estimate_parameter_count(code),
        "estimated_complexity": _estimate_complexity(code),
    }


def compare_metrics(original_code: str, refactored_code: str) -> Dict[str, Any]:
    before = compute_code_metrics(original_code)
    after = compute_code_metrics(refactored_code)
    return {
        "loc_before": before["loc"],
        "loc_after": after["loc"],
        "complexity_before": before["estimated_complexity"],
        "complexity_after": after["estimated_complexity"],
        "parameter_count_before": before["parameter_count"],
        "parameter_count_after": after["parameter_count"],
    }
