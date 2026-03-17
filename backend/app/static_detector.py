import re

def detect_static(code):

    smells = []

    # 1. Magic Number
    if re.search(r"\b\d{2,}\b", code):
        smells.append("Magic Number")

    # 2. Missing Default
    if "switch" in code and "default" not in code:
        smells.append("Missing Default")

    # 3. Empty Catch Clause
    if re.search(r"catch\s*\(.*\)\s*\{\s*\}", code):
        smells.append("Empty Catch Clause")

    # 4. Long Parameter List (>4 parameters)
    if re.search(r"\(.*?,.*?,.*?,.*?,.*?\)", code):
        smells.append("Long Parameter List")

    # 5. Long Identifier (>20 characters)
    if re.search(r"\b[a-zA-Z_]{20,}\b", code):
        smells.append("Long Identifier")

    # 6. Duplicate Code (simple repeated lines)
    lines = code.split("\n")
    if len(lines) != len(set(lines)):
        smells.append("Duplicate Code")

    # 7. Complex Conditional (nested if)
    if len(re.findall(r"\bif\b", code)) > 3:
        smells.append("Complex Conditional")

    # 8. Long Statement (very long line)
    for line in lines:
        if len(line) > 120:
            smells.append("Long Statement")
            break

    # 9. Complex Method (many conditions + loops)
    if len(re.findall(r"\b(for|while|if)\b", code)) > 10:
        smells.append("Complex Method")

    # 10. Large Class (rough check using line count)
    if len(lines) > 300:
        smells.append("Large Class")

    return list(set(smells))