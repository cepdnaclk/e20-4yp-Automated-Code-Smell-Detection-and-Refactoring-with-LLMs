import json
import re
from pathlib import Path
from typing import Dict, List, Optional

from config import BASE_DIR

EXAMPLES_DIR = BASE_DIR / "examples"
MAX_EXAMPLES = 5
WORD_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

STRATEGY_ALIAS = {
    "move_field": "move_method",
    "inline_method_or_class": "extract_method",
    "encapsulate_field": "extract_class",
    "remove_dead_code": "extract_method",
    "reduce_coupling": "move_method",
    "replace_inheritance_with_delegation": "extract_class",
    "split_responsibilities": "extract_class",
    "replace_primitive_with_value_object": "introduce_parameter_object",
    "replace_conditional_with_polymorphism": "decompose_conditional",
}

GENERIC_BY_STRATEGY = {
    "extract_method": [
        ("def f(items):\n    total = 0\n    for i in items:\n        if i > 0:\n            total += i\n    return total", "def f(items):\n    return positive_total(items)\n\n\ndef positive_total(items):\n    total = 0\n    for i in items:\n        if i > 0:\n            total += i\n    return total", "Extracts cohesive loop logic into a helper."),
        ("def g(users):\n    names = []\n    for user in users:\n        if user.active:\n            names.append(user.name)\n    return names", "def g(users):\n    return active_names(users)\n\n\ndef active_names(users):\n    names = []\n    for user in users:\n        if user.active:\n            names.append(user.name)\n    return names", "Separates collection logic from orchestration."),
        ("def h(rows):\n    result = []\n    for row in rows:\n        if row.valid:\n            result.append(row.id)\n    return result", "def h(rows):\n    return valid_ids(rows)\n\n\ndef valid_ids(rows):\n    result = []\n    for row in rows:\n        if row.valid:\n            result.append(row.id)\n    return result", "Shortens the main function without changing behavior."),
    ],
    "extract_class": [
        ("class Manager:\n    def total(self, items):\n        return sum(item.price for item in items)\n\n    def export(self, items):\n        return '\\n'.join(str(item.price) for item in items)", "class Manager:\n    def __init__(self):\n        self.exporter = Exporter()\n\n    def total(self, items):\n        return sum(item.price for item in items)\n\n    def export(self, items):\n        return self.exporter.export(items)\n\n\nclass Exporter:\n    def export(self, items):\n        return '\\n'.join(str(item.price) for item in items)", "Moves a secondary responsibility into a focused class."),
        ("class Service:\n    def save(self, item):\n        print('saved')\n\n    def notify(self, item):\n        print(item.email)", "class Service:\n    def __init__(self):\n        self.notifier = Notifier()\n\n    def save(self, item):\n        print('saved')\n\n    def notify(self, item):\n        self.notifier.notify(item)\n\n\nclass Notifier:\n    def notify(self, item):\n        print(item.email)", "Extracts notification behavior from persistence behavior."),
        ("class Catalog:\n    def add(self, item):\n        pass\n\n    def print_labels(self, items):\n        for item in items:\n            print(item.name)", "class Catalog:\n    def __init__(self):\n        self.printer = LabelPrinter()\n\n    def add(self, item):\n        pass\n\n    def print_labels(self, items):\n        self.printer.print_labels(items)\n\n\nclass LabelPrinter:\n    def print_labels(self, items):\n        for item in items:\n            print(item.name)", "Improves cohesion by moving printing into a collaborator."),
    ],
    "move_method": [
        ("class S:\n    def summary(self, customer):\n        return customer.name + ' ' + customer.tier", "class S:\n    def summary(self, customer):\n        return customer.summary()\n\n\nclass Customer:\n    def summary(self):\n        return self.name + ' ' + self.tier", "Moves behavior to the class that owns the data."),
        ("class Payroll:\n    def annual(self, employee):\n        return employee.salary * 12", "class Payroll:\n    def annual(self, employee):\n        return employee.annual_salary()\n\n\nclass Employee:\n    def annual_salary(self):\n        return self.salary * 12", "Reduces feature envy by relocating salary logic."),
        ("class V:\n    def city(self, order):\n        return order.customer.address.city", "class V:\n    def city(self, order):\n        return order.city()\n\n\nclass Order:\n    def city(self):\n        return self.customer.address.city", "Moves navigation logic closer to the object graph."),
    ],
    "introduce_parameter_object": [
        ("def create(a, b, c, d):\n    return [a, b, c, d]", "class Args:\n    def __init__(self, a, b, c, d):\n        self.a = a\n        self.b = b\n        self.c = c\n        self.d = d\n\n\ndef create(args):\n    return [args.a, args.b, args.c, args.d]", "Groups related inputs into one object."),
        ("def book(date, time, room, host):\n    return [date, time, room, host]", "class Booking:\n    def __init__(self, date, time, room, host):\n        self.date = date\n        self.time = time\n        self.room = room\n        self.host = host\n\n\ndef book(details):\n    return [details.date, details.time, details.room, details.host]", "Simplifies a long parameter list."),
        ("def ship(name, street, city, zip_code):\n    return f'{name},{street},{city},{zip_code}'", "class Address:\n    def __init__(self, name, street, city, zip_code):\n        self.name = name\n        self.street = street\n        self.city = city\n        self.zip_code = zip_code\n\n\ndef ship(address):\n    return f'{address.name},{address.street},{address.city},{address.zip_code}'", "Creates a value object for a parameter cluster."),
    ],
    "decompose_conditional": [
        ("def discount(kind, total):\n    if kind == 'VIP' and total > 100 or kind == 'REG' and total > 200:\n        return 10\n    return 0", "def discount(kind, total):\n    if eligible_for_discount(kind, total):\n        return 10\n    return 0\n\n\ndef eligible_for_discount(kind, total):\n    return (kind == 'VIP' and total > 100) or (kind == 'REG' and total > 200)", "Extracts a complex rule into a named predicate."),
        ("def shipping(i, q):\n    if i and q < 10 or (not i and q < 5):\n        return 20\n    return 5", "def shipping(i, q):\n    if requires_high_shipping(i, q):\n        return 20\n    return 5\n\n\ndef requires_high_shipping(i, q):\n    return (i and q < 10) or ((not i) and q < 5)", "Makes branching intent explicit."),
        ("def access(user, resource):\n    if user.admin or (user.member and not resource.archived):\n        return True\n    return False", "def access(user, resource):\n    return has_access(user, resource)\n\n\ndef has_access(user, resource):\n    return user.admin or (user.member and not resource.archived)", "Turns a dense conditional into a readable helper."),
    ],
}


def _normalize_strategy_name(strategy: str) -> str:
    return strategy.strip().lower()


def _canonical_strategy(strategy: str) -> str:
    normalized = _normalize_strategy_name(strategy)
    return STRATEGY_ALIAS.get(normalized, normalized)


def _slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def _tokenize(text: str) -> set:
    return {token.lower() for token in WORD_RE.findall(text or "")}


def _jaccard_score(left: set, right: set) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _load_examples(path: Path) -> List[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, list) else [data]


def _generated_examples(strategy: str, smell_type: str) -> List[dict]:
    canonical = _canonical_strategy(strategy)
    examples = []
    for before, after, why in GENERIC_BY_STRATEGY.get(canonical, []):
        examples.append({"smell": smell_type, "strategy": strategy, "before": before, "after": after, "why": why})
    return examples


def _candidate_paths(language: str, strategy: str, smell_type: str) -> List[Path]:
    canonical = _canonical_strategy(strategy)
    smell_slug = _slugify(smell_type)
    return [
        EXAMPLES_DIR / language.lower() / "smells" / f"{smell_slug}.json",
        EXAMPLES_DIR / "smells" / f"{smell_slug}.json",
        EXAMPLES_DIR / language.lower() / f"{canonical}.json",
        EXAMPLES_DIR / f"{canonical}.json",
    ]


def _dedupe_examples(examples: List[dict]) -> List[dict]:
    seen = set()
    unique = []
    for example in examples:
        key = (
            example.get("smell", ""),
            example.get("strategy", ""),
            example.get("before", ""),
            example.get("after", ""),
        )
        if key in seen:
            continue
        seen.add(key)
        unique.append(example)
    return unique


def _example_similarity_score(
    example: dict,
    strategy: str,
    smell_type: str,
    target_code: str,
    location: str,
    metrics: Optional[Dict[str, object]],
) -> float:
    score = 0.0
    example_smell = str(example.get("smell", ""))
    example_strategy = str(example.get("strategy", ""))

    if example_smell == smell_type:
        score += 60.0
    elif _slugify(example_smell) == _slugify(smell_type):
        score += 45.0

    if _canonical_strategy(example_strategy) == _canonical_strategy(strategy):
        score += 30.0

    target_tokens = _tokenize(target_code)
    before_tokens = _tokenize(example.get("before", ""))
    after_tokens = _tokenize(example.get("after", ""))
    score += _jaccard_score(target_tokens, before_tokens) * 18.0
    score += _jaccard_score(target_tokens, after_tokens) * 10.0

    location_tokens = _tokenize(location)
    if location_tokens:
        score += _jaccard_score(location_tokens, before_tokens | after_tokens) * 12.0

    metric_tokens = _tokenize(" ".join(str(key) for key in (metrics or {}).keys()))
    if metric_tokens:
        score += _jaccard_score(metric_tokens, before_tokens | after_tokens) * 6.0

    if example.get("adapted_from_real_world"):
        score += 2.0
    return score


def select_examples(
    language: str,
    strategy: str,
    smell_type: str,
    target_code: str = "",
    location: str = "",
    metrics: Optional[Dict[str, object]] = None,
    max_examples: int = MAX_EXAMPLES,
) -> List[dict]:
    candidates: List[dict] = []
    for path in _candidate_paths(language, strategy, smell_type):
        candidates.extend(_load_examples(path))

    candidates = _dedupe_examples(candidates)
    ranked = sorted(
        candidates,
        key=lambda example: _example_similarity_score(
            example,
            strategy,
            smell_type,
            target_code,
            location,
            metrics,
        ),
        reverse=True,
    )
    selected = ranked[:max_examples]
    if len(selected) < max_examples:
        selected = _dedupe_examples(selected + _generated_examples(strategy, smell_type))[:max_examples]
    return selected


def format_examples(examples: List[dict]) -> str:
    if not examples:
        return "No few-shot examples available for this refactoring."
    blocks = []
    for index, example in enumerate(examples, start=1):
        blocks.append(
            f"Example {index}\n"
            f"Smell: {example.get('smell', 'Unknown')}\n"
            f"Strategy: {example.get('strategy', 'Unknown')}\n"
            f"BEFORE:\n{example.get('before', '')}\n\n"
            f"AFTER:\n{example.get('after', '')}\n\n"
            f"Why this works: {example.get('why', 'No rationale provided.')}"
        )
    return "\n\n".join(blocks)




