import re
from typing import Any, Dict

DEFAULT_CONTEXT_LINES = 12
MAX_SCOPE_LINES = 80


def _clamp_scope_size(metrics: Dict[str, Any]) -> int:
    loc = metrics.get("loc") or metrics.get("lines") or metrics.get("method_loc")
    try:
        numeric_loc = int(loc)
    except (TypeError, ValueError):
        numeric_loc = 0
    base = max(DEFAULT_CONTEXT_LINES, numeric_loc + 8)
    return min(base, MAX_SCOPE_LINES)

def _extract_by_line_hint(lines, location: str, scope_size: int):
    line_match = re.search(r"line\s*(\d+)", location, re.IGNORECASE)
    if not line_match:
        return ""
    line_number = int(line_match.group(1)) - 1
    start = max(0, line_number - scope_size // 2)
    end = min(len(lines), line_number + scope_size // 2)
    return "\n".join(lines[start:end]).strip()

def _extract_by_symbol_hint(code: str, location: str, scope_size: int):
    lines = code.splitlines()
    if not location or location.lower() == "unknown":
        return ""

    direct = _extract_by_line_hint(lines, location, scope_size)
    if direct:
        return direct

    candidates = [segment.strip() for segment in re.split(r"[\s:()\-.]+", location) if segment.strip()]
    for candidate in sorted(candidates, key=len, reverse=True):
        match = re.search(re.escape(candidate), code)
        if not match:
            continue
        start_line = code[: match.start()].count("\n")
        start = max(0, start_line - scope_size // 3)
        end = min(len(lines), start_line + scope_size)
        return "\n".join(lines[start:end]).strip()
    return ""

def extract_focus_scope(code: str, location: str, metrics: Dict[str, Any]) -> str:
    lines = code.splitlines()
    if not lines:
        return code

    scope_size = _clamp_scope_size(metrics)
    focused = _extract_by_symbol_hint(code, location or "", scope_size)
    if focused:
        return focused

    fallback_end = min(len(lines), scope_size)
    return "\n".join(lines[:fallback_end]).strip()

def build_scope_note(location: str, focused_scope: str, full_code: str) -> str:
    if not focused_scope:
        return "Focused scope unavailable; use the original code conservatively."
    if focused_scope.strip() == full_code.strip():
        return "Focused scope matched the full file; refactor conservatively and return the full file."
    location_label = location or "the detected smell location"
    return (
        f"Focused scope extracted around {location_label}. Use it to localize the change, "
        "but return the full refactored file."
    )
