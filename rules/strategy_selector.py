from typing import Any, Dict, List, Optional

from rules.smell_catalog import SMELL_CATALOG


SEVERITY_RANK = {
    "Critical": 0,
    "Major": 1,
    "Moderate": 2,
    "Minor": 3,
    "Low": 4,
}

ALIASES = {
    "Blob": "Blob (God Class)",
    "God Class": "Blob (God Class)",
    "Long Function": "Long Method",
}


def load_catalog() -> Dict[str, Dict[str, Any]]:
    return SMELL_CATALOG


def normalize_smell_name(smell_name: str) -> str:
    cleaned = smell_name.strip()
    return ALIASES.get(cleaned, cleaned)


def get_strategy(smell_name: str, catalog: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]:
    catalog = catalog or load_catalog()
    normalized_name = normalize_smell_name(smell_name)
    entry = catalog.get(normalized_name)
    if not entry:
        return {
            "category": "unknown",
            "group": "unknown",
            "primary_strategy": "extract_method",
            "fallback_strategies": [],
            "validation_level": "syntax",
            "priority": 99,
        }
    return entry


def sort_smells(smells: List[Dict[str, Any]], catalog: Optional[Dict[str, Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    catalog = catalog or load_catalog()

    def sort_key(smell: Dict[str, Any]) -> Any:
        strategy = get_strategy(smell["type"], catalog)
        severity_rank = SEVERITY_RANK.get(smell.get("severity", "Moderate"), 5)
        return (strategy.get("priority", 99), severity_rank, smell["type"])

    return sorted(smells, key=sort_key)
