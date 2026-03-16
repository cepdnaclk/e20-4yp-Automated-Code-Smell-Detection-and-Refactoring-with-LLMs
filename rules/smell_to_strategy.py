from rules.strategy_selector import get_strategy, load_catalog, normalize_smell_name


_CATALOG = load_catalog()

SMELL_TO_STRATEGY = {
    smell_name: metadata["primary_strategy"].replace("_", " ").title()
    for smell_name, metadata in _CATALOG.items()
}


def should_auto_refactor(severity):
    return severity in ["Major", "Critical", "Moderate"]


def get_refactoring_strategy(smell_name):
    normalized_name = normalize_smell_name(smell_name)
    strategy = get_strategy(normalized_name, _CATALOG)
    return strategy["primary_strategy"]
